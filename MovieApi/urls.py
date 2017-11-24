from django.conf.urls import url
from .api import *

urlpatterns = [
    url(r'^movie/(?P<pk>\d+)/$', MovieDetails.as_view()),
    url(r'^list/will_watch/movie/(?P<pk>\d+)/$', AddMovieInListWillWatch.as_view()),
    url(r'^list/already_watched/movie/(?P<pk>\d+)/$', AddMovieInListAlreadyWatched.as_view()),
    url(r'^list/will_watch/$', MoviesWillWatch.as_view()),
    url(r'^list/already_watched/$', MoviesAlreadyWatched.as_view()),
    #url(r'^movies/filter/emoji/$', MoviesFilterByEmoji.as_view()),
    url(r'^user/add/friend/$', AddFriend.as_view()),
    url(r'^user/(?P<token>[0-9a-zA-Z_-]+)/$', UserDetails.as_view()),
]