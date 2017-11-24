from django.conf.urls import url
from .api import *

urlpatterns = [
    url(r'^movie/(?P<pk>\d+)/$', MovieDetails.as_view()),
    url(r'^list/will_watch/movie/(?P<pk>\d+)/$', AddMovieInListWillWatch.as_view()),
    url(r'^list/already_watched/movie/(?P<pk>\d+)/$', AddMovieInListAlreadyWatched.as_view()),
]