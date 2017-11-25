# -*- coding: utf-8 -*-
from django.db import models

from django.db import models
import uuid
import os


def get_file_path_avatar(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('images/avatars', filename)


class Genre(models.Model):
    class Meta:
        db_table = 'genres'

    name_en = models.TextField(null=True)


class ProductionCompany(models.Model):
    class Meta:
        db_table = 'production_companies'

    name_en = models.TextField(null=True)


class ProductionCountry(models.Model):
    class Meta:
        db_table = 'production_countries'

    iso_3166_1 = models.TextField(null=True)
    name_en = models.TextField(null=True)


class SpokenLanguage(models.Model):
    class Meta:
        db_table = 'spoken_languages'

    iso_639_1 = models.TextField(null=True)
    name = models.TextField(null=True)


class Collection(models.Model):
    class Meta:
        db_table = 'collections'

    name_en = models.TextField(null=True)
    poster_path = models.TextField(null=True)
    backdrop_path = models.TextField(null=True)


class Cast(models.Model):
    class Meta:
        db_table = 'cast'

    character = models.TextField(null=True)
    name = models.TextField(null=True)
    order = models.IntegerField(null=True)
    profile_path = models.TextField(null=True)


class Crew(models.Model):
    class Meta:
        db_table = 'crew'

    department = models.TextField(null=True)
    name = models.TextField(null=True)
    job = models.TextField(null=True)
    profile_path = models.TextField(null=True)


class Backdrop(models.Model):
    class Meta:
        db_table = 'backdrop'

    aspect_ratio = models.FloatField(null=True)
    file_path = models.TextField(null=True)
    height = models.IntegerField(null=True)
    iso_639_1 = models.TextField(null=True)
    vote_average = models.IntegerField()
    vote_count = models.IntegerField(null=True)
    width = models.IntegerField(null=True)


class Poster(models.Model):
    class Meta:
        db_table = 'poster'

    aspect_ratio = models.FloatField(null=True)
    file_path = models.TextField(null=True)
    height = models.IntegerField(null=True)
    iso_639_1 = models.TextField(null=True)
    vote_average = models.IntegerField(null=True)
    vote_count = models.IntegerField(null=True)
    width = models.IntegerField(null=True)


class Emoji(models.Model):
    class Meta:
        db_table = 'emoji'

    description_code = models.TextField(null=True)
    description_en = models.TextField(null=True)
    code = models.TextField(null=True)
    type = models.TextField(null=True)


class Movie(models.Model):
    class Meta:
        db_table = 'movies'

    backdrop_path = models.TextField(null=True)
    belongs_to_collection = models.ManyToManyField(Collection, blank=True)
    budget = models.BigIntegerField(null=True)
    genres = models.ManyToManyField(Genre, blank=True)
    genre_main = models.TextField(null=True)
    genre_rus_1 = models.TextField(null=True)
    genre_rus_2 = models.TextField(null=True)
    genre_rus_3 = models.TextField(null=True)
    genre_rus_4 = models.TextField(null=True)
    genre_rus_5 = models.TextField(null=True)
    genre_rus_6 = models.TextField(null=True)
    genre_rus_7 = models.TextField(null=True)
    genre_rus_8 = models.TextField(null=True)
    genre_rus_9 = models.TextField(null=True)
    genre_rus_10 = models.TextField(null=True)
    imdb_id = models.TextField(null=True)
    original_language = models.TextField(null=True)
    overview_en = models.TextField(null=True)
    popularity = models.FloatField()
    poster_path = models.TextField(null=True)
    production_companies = models.ManyToManyField(ProductionCompany, blank=True)
    production_countries = models.ManyToManyField(ProductionCountry, blank=True)
    production_country_main = models.TextField(null=True)
    release_year = models.TextField(null=True)
    revenue = models.BigIntegerField(null=True)
    runtime = models.IntegerField(null=True)
    spoken_languages = models.ManyToManyField(SpokenLanguage, blank=True)
    status = models.TextField(null=True)
    tagline_en = models.TextField(null=True)
    title_en = models.TextField(null=True)
    vote_average = models.FloatField()
    vote_count = models.IntegerField(default=30)
    cast = models.ManyToManyField(Cast, blank=True)
    crew = models.ManyToManyField(Crew, blank=True)
    backdrops = models.ManyToManyField(Backdrop, blank=True)
    posters = models.ManyToManyField(Poster, blank=True)
    emoji = models.ManyToManyField(Emoji, related_name='movies', blank=True)


class User(models.Model):
    class Meta:
        db_table = 'users'

    avatar = models.ImageField(upload_to=get_file_path_avatar, blank=True)
    token = models.TextField(null=True)
    username = models.TextField(null=True)
    facebook_uid = models.TextField(null=True)
    movies_will_watch = models.ManyToManyField(Movie, blank=True, related_name='movies_will_watch_1')
    movies_not_show = models.ManyToManyField(Movie, blank=True, related_name='movies_not_show_1')
    friends = models.ManyToManyField("self", blank=True)


class MovieAlreadyWatched(models.Model):
    class Meta:
        db_table = 'movies_already_watched'

    movie = models.ManyToManyField(Movie, blank=True)
    user = models.ManyToManyField(User, blank=True)
    rate = models.IntegerField(null=True)


class EmojiFace(models.Model):
    class Meta:
        db_table = 'emoji_face'

    description_code = models.TextField(null=True)
    description = models.TextField(null=True)
    code = models.TextField(null=True)
    value = models.FloatField(default=0)


#Голос пользователя
class UserVote(models.Model):
    class Meta:
        db_table = 'user_vote'

    movie = models.OneToOneField(Movie, blank=True, null=True)
    user = models.OneToOneField(User, blank=True, null=True)


#Голосование
class Voting(models.Model):
    class Meta:
        db_table = 'voting'

    participant = models.ManyToManyField(User, blank=True, related_name='voting')
    movie = models.ManyToManyField(Movie, blank=True, related_name='voting_m')
    vote = models.ManyToManyField(UserVote, blank=True, related_name='voting')

