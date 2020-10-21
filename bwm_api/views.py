import json
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from bwm_api.models import UserData, UserSerializer
from recommenders.models import MoviesData, MoviesSerializer


@api_view(['GET', 'POST'])
def user_info(request, user_id):
    if request.method == 'GET':
        try:
            user = UserData.objects.filter(pk=user_id)
            serializer = UserSerializer(user)
        except UserData.DoesNotExist:
            return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def user_recommend_genre(request, user_id):
    try:
        user = UserData.objects.filter(pk=user_id)
        serializer = UserSerializer(user)     
    except UserData.DoesNotExist:
        return Response(serializer.data, status=status.HTTP_404_NOT_FOUND)
    
    reco = serializer.data['data'].get('genres')
    reco = reco.values()
    if not reco:
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

    movies = MoviesSerializer(MoviesData.manager.all(), many=True)
    result = []
    for movie in movies:
        genres = json.dumps(movie.data['genres'])
        for r in reco:
            if r in genres:
                result.append(movie.data)
    
    return Response({'recommendations': result}, status=status.HTTP_200_OK)