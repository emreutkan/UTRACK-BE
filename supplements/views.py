from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Supplement, UserSupplement, UserSupplementLog
from .serializers import SupplementSerializer, UserSupplementSerializer, UserSupplementLogSerializer

class SupplementListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
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

  