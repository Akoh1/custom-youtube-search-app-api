import http
from urllib import response
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from searchapi.models.user import User
from searchapi.models.comments import Comment
from ..serializers.auth import UserSerializer
from searchapi.serializers.comments import CommentSerializer
import json
from rest_framework.renderers import JSONRenderer
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
from django.contrib.auth import authenticate

class CommentDetailView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    renderer_classes = [JSONRenderer]

    def get_object(self, pk, token):
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            try:
                user = get_object_or_404(User, id=payload['id'])
                return Comment.objects.get(pk=pk, user=user.id)
            except Comment.DoesNotExist:
                raise Http404
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthorized!')

    def get(self, request, pk, format=None):
        token = request.COOKIES.get('jwt')

        comment = self.get_object(pk, token)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        token = request.COOKIES.get('jwt')

        comment = self.get_object(pk, token)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        token = request.COOKIES.get('jwt')
        comment = self.get_object(pk, token)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class CommentListView(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    renderer_classes = [JSONRenderer]

    def get_current_user(self, token):
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            try:
                user = get_object_or_404(User, id=payload['id'])
                return user
            except User.DoesNotExist:
                raise Http404
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthorized!')

    def get_object(self, token):
        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])

            try:
                user = get_object_or_404(User, id=payload['id'])
                return Comment.objects.filter(user=user.id)
            except Comment.DoesNotExist:
                raise Http404
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthorized!')

    def get(self, request, format=None):
        token = request.COOKIES.get('jwt')

        comment = self.get_object(token)
        serializer = CommentSerializer(comment, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        token = request.COOKIES.get('jwt')
        user = self.get_current_user(token)

        data = request.data
        data['user'] = user.id
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




