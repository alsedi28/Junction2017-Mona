# -*- coding: utf-8 -*-
from rest_framework import generics
from .serializers import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
import time
import requests
import pandas as pd
import numpy as np
import base64

class MovieDetails(generics.RetrieveAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def get_queryset(self):
        try:
            return self.queryset.filter(id=self.kwargs.get('pk'))
        except ObjectDoesNotExist:
            return Response({"status": "the movie doesn't exist"}, status=400)


class AddMovieInListWillWatch(generics.CreateAPIView):
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        if 'token' not in request.POST.keys() or request.POST['token'] == "":
            return Response({"status": "parameter token is empty"}, status=400)

        movie_id = self.kwargs.get('pk')
        token = request.POST['token']

        try:
            user = User.objects.get(token=token)
            movie = Movie.objects.get(id=movie_id)

            if len(user.movies_will_watch.filter(id=movie_id)) == 0:
                user.movies_will_watch.add(movie)

        except ObjectDoesNotExist:
            return Response({"status": "either the user or movie doesn't exist."}, status=400)
        except Exception:
            return Response({"status": "unexpected error"}, status=400)

        return Response({"status": "ok"}, status=200)


class AddMovieInListAlreadyWatched(generics.CreateAPIView):
    serializer_class = MovieSerializer

    def post(self, request, *args, **kwargs):
        if 'token' not in request.POST.keys() or request.POST['token'] == "":
            return Response({"status": "parameter token is empty"}, status=400)
        if 'rate' not in request.POST.keys() or request.POST['rate'] == "":
            return Response({"status": "parameter rate is empty"}, status=400)

        movie_id = self.kwargs.get('pk')
        rate = int(request.POST['rate'])
        token = request.POST['token']

        try:
            user = User.objects.get(token=token)
            movie = Movie.objects.get(id=movie_id)

            if rate > 10:
                rate = 10
            elif rate < 0:
                rate = 0

            current_vote_average = movie.vote_average
            current_vote_count = movie.vote_count

            movie.vote_count = current_vote_count + 1
            movie.vote_average = (current_vote_average * current_vote_count + rate) / (current_vote_count + 1)
            movie.save()

            if len(MovieAlreadyWatched.objects.filter(movie=movie, user=user)) == 0:
                movie_already_watched = MovieAlreadyWatched.objects.create(rate=rate)
                movie_already_watched.movie.add(movie)
                movie_already_watched.user.add(user)

        except ObjectDoesNotExist:
            return Response({"status": "either the user or movie doesn't exist."}, status=400)
        except Exception:
            return Response({"status": "unexpected error"}, status=400)

        return Response({"status": "ok"}, status=200)


class MoviesAlreadyWatched(generics.ListAPIView):
    serializer_class = MovieAlreadyWatchedSerializer
    queryset = Movie.objects.all()

    def get_queryset(self):
        if 'token' not in self.request.GET.keys():
            return Response({"status": "parameter token is empty"}, status=400)

        token = self.request.GET['token']
        try:
            user = User.objects.get(token=token)

            movies_id_sorted_list = MovieAlreadyWatched.objects.filter(user=user).order_by('-rate').values_list(
                'movie__id', flat=True)
            user_movies = Movie.objects.filter(id__in=movies_id_sorted_list)
            movies = dict([(obj.id, obj) for obj in user_movies])
            sorted_movies = [movies[id] for id in movies_id_sorted_list]

            return sorted_movies

        except ObjectDoesNotExist:
            return Response({"status": "the user doesn't exist."}, status=400)

    def get_serializer_context(self):
        context = super(self.__class__,
                        self).get_serializer_context()  # if python 3 change super().get_serializer_context()
        if 'token' not in self.request.GET.keys() or self.request.GET['token'] == "":
            return context

        context['token'] = self.request.GET['token']

        return context


class MoviesWillWatch(generics.ListAPIView):
    serializer_class = MovieWillWatchSerializer
    queryset = Movie.objects.all()

    def get_queryset(self):
        if 'token' not in self.request.GET.keys():
            return Response({"status": "parameter token is empty"}, status=400)

        token = self.request.GET['token']
        try:
            user = User.objects.get(token=token)

            movies_id_sorted_list = Movie.movies_will_watch_1.through.objects.filter(user_id=user.id).order_by(
                '-id').values_list('movie_id', flat=True)
            user_movies = Movie.objects.filter(id__in=movies_id_sorted_list)
            movies = dict([(obj.id, obj) for obj in user_movies])
            sorted_movies = [movies[id] for id in movies_id_sorted_list]

            return sorted_movies
        except ObjectDoesNotExist:
            return Response({"status": "the user doesn't exist."}, status=400)


class AddFriend(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        if 'token' not in request.POST.keys() or request.POST['token'] == "":
            return Response({"status": "parameter token is empty"}, status=400)

        if 'user_id' not in request.POST.keys() or request.POST['user_id'] == "":
            return Response({"status": "parameter user_id is empty"}, status=400)

        user_id = request.POST['user_id']
        token = request.POST['token']

        try:
            user = User.objects.get(token=token)
            friend = User.objects.get(id=user_id)

            if len(user.friends.filter(id=user_id)) == 0:
                user.friends.add(friend)

        except ObjectDoesNotExist:
            return Response({"status": "either the user or friend doesn't exist."}, status=400)
        except Exception:
            return Response({"status": "unexpected error"}, status=400)

        return Response({"status": "ok"}, status=200)


class UserDetails(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    lookup_field = 'token'
    queryset = User.objects.all()


class EmojiFaceByPhoto(generics.ListAPIView):
    queryset = EmojiFace.objects.all()

    def post(self, request, *args, **kwargs):
        if 'image' not in request.POST.keys() or request.POST['image'] == "":
            return Response({"status": "parameter image is empty"}, status=400)

        headers = dict()
        headers['Ocp-Apim-Subscription-Key'] = _key
        headers['Content-Type'] = 'application/octet-stream'

        result = processRequest(base64.b64decode(request.POST['image']), headers)
        if result is None:
            return Response({"status": "unexpected error"}, status=400)

        result_dict = dict()
        result_list = []
        for i in result.index:
            result_dict[i] = result[i]
            result_list.append(i)

        emoji = list(EmojiFace.objects.filter(description__in=result_list))

        for i in emoji:
            i.value = result_dict[i.description]

        return Response(EmojiFaceSerializer(emoji, many=True).data)

#Helpers
_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
_key = '8109829b80824cccb74cf36c36d62d97' #primary key
_maxNumRetries = 10

def processRequest(data, headers):
    retries = 0
    result = None

    while True:
        response = requests.request('post', _url, json=None, data=data, headers=headers, params=None)

        if response.status_code == 429:
            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                    sq = pd.Series([face['faceRectangle']['width'] * face['faceRectangle']['height'] for face in result])
                    sq = sq.astype(float)/sq.sum()

                    sc = np.array([sq[i] * np.array(face['scores'].values()) for i, face in enumerate(result)])
                    sc = pd.Series(data=np.sum(sc, axis=0), index=result[0]['scores'].keys()).sort_values(ascending=False)
                    if sc[0] < 0.9:
                        tmp = sc[:2]
                        result = tmp.apply(lambda x: x/sum(tmp))
                    else:
                        result = sc[:1]
        break

    return result