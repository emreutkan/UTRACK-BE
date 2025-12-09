from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Supplement, UserSupplement, UserSupplementLog
from .serializers import SupplementSerializer, UserSupplementSerializer, UserSupplementLogSerializer
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Q
class SupplementListView(APIView):
    permission_classes = [IsAuthenticated]

    # Cache this view for 15 minutes (60 seconds * 15) 
    # django keeps cached data in memory for 15 minutes so it doesn't have to hit the database every time
    # for multiple servers in production we can use redis to cache the data
    @method_decorator(cache_page(60*15))
    def get(self, request):
        query = request.query_params.get('search', None)
        if query:
            supplements = supplements.filter(
                Q(name__icontains=query) | Q(description__icontains=query)
            )
        else:
            supplements = Supplement.objects.filter(is_active=True)
        serializer = SupplementSerializer(supplements, many=True)
        return Response(serializer.data)

class UserSupplementListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_supplements = UserSupplement.objects.filter(user=request.user, is_active=True)
        serializer = UserSupplementSerializer(user_supplements, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSupplementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSupplementLogListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_supplement_logs = UserSupplementLog.objects.filter(user=request.user, is_active=True)
        serializer = UserSupplementLogSerializer(user_supplement_logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSupplementLogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

  
class UserSupplementLogDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, log_id):
        user_supplement_log = UserSupplementLog.objects.get(id=log_id, user=request.user, is_active=True)
        user_supplement_log.is_active = False
        user_supplement_log.save()
        return Response(status=status.HTTP_204_NO_CONTENT)