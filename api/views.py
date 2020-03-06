from django.shortcuts import render

from django.http import HttpResponse, JsonResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from api.models import Comment, Community
from api.serializers import (CommentSerializer, CommunityWriteSerializer)
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


def comment_list(request, community):
    if request.method == 'GET':
        comments = Comment.objects.get_community_comments(community)
        serializer = CommentSerializer(comments, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'POST'])
# def get_post_community(request):
#     if request.method == 'GET':
#         communities = Community.objects.all()
#         serializer = CommunityReadSerializer(communities, many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
#         data = JSONParser().parse(request)
#         serializer = CommunityWriteSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateCommunity(CreateAPIView):
    queryset = Community.objects.all()
    serializer_class = CommunityWriteSerializer
    # permission_classes = [IsAuthenticated]
