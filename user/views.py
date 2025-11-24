

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterView(APIView):
    serializer_class = RegisterSerializer  # 
    def post(self, request):

        serializer = RegisterSerializer(data=request.data)  # 1. Grab the data the user sent (JSON) and pass it to our serializer

        if serializer.is_valid(): # 2. Validate data against Model rules (unique email, max_length) and Field types (valid email format)


            # TODO: Send verification email
            
            user = serializer.save() ## Save the user to the database
            refresh = RefreshToken.for_user(user) ## Generate JWT tokens
            return Response({           
                'refresh': str(refresh),
                'access': str(refresh.access_token) ## Return the JWT tokens
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) ## Return the errors if the serializer is not valid