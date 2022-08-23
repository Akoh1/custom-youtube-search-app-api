import http
from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from searchapi.models.user import User
from ..serializers.auth import UserSerializer
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.contrib.auth import authenticate

# Create your views here.

# class UserJSONRenderer(JSONRenderer):
#     charset = 'utf-8'

#     def render(self, data, media_type=None, renderer_context=None):
#         # If we receive a `token` key as part of the response, it will be a
#         # byte object. Byte objects don't serialize well, so we need to
#         # decode it before rendering the User object.
#         token = data.get('token', None)

#         if token is not None and isinstance(token, bytes):
#             # Also as mentioned above, we will decode `token` if it is of type
#             # bytes.
#             data['token'] = token.decode('utf-8')

#         # Finally, we can render our data under the "user" namespace.
#         return json.dumps({
#             'user': data
#         })


class RegisterView(APIView):
    # renderer_classes = (UserJSONRenderer,)
    # def get(self, request, format=None):
    #     snippets = Snippet.objects.all()
    #     serializer = SnippetSerializer(snippets, many=True)
    #     return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, format=None):
        email = request.data['email']
        password = request.data['password']

        # user = User.objects.filter(email=email).first()
        user = authenticate(username=email, password=password)

        if user is None:
            raise AuthenticationFailed("user not found")

        if not user.check_password(password):
            raise AuthenticationFailed('incorrect password')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')
        # token = jwt.decode(encoded, "secret", algorithms=["HS256"])
        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "message": "success",
            "jwt": token
        }
        return response


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        # user = get_object_or_404(User, id=payload['id'])
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response =  Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
        return response