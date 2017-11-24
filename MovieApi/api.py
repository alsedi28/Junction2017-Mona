# -*- coding: utf-8 -*-
from rest_framework import generics
from .serializers import *
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response


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
