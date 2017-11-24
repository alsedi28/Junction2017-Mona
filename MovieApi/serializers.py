from rest_framework import serializers
from .models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name_en')


class ProductionCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCompany
        fields = ('id', 'name_en')


class ProductionCountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductionCountry
        fields = ('id', 'name_en', 'iso_3166_1')


class SpokenLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpokenLanguage
        fields = ('id', 'name', 'iso_639_1')


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ('id', 'name_en', 'poster_path', 'backdrop_path')


class CastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cast
        fields = ('id', 'name', 'character', 'order', 'profile_path')


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ('id', 'name', 'department', 'job', 'profile_path')


class BackdropSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backdrop
        fields = ('id', 'aspect_ratio', 'file_path', 'height', 'iso_639_1', 'vote_average', 'vote_count', 'width')


class PosterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poster
        fields = ('id', 'aspect_ratio', 'file_path', 'height', 'iso_639_1', 'vote_average', 'vote_count', 'width')


class EmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emoji
        fields = ('id', 'description_en', 'code', 'type')


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True)
    production_companies = ProductionCompanySerializer(many=True)
    production_countries = ProductionCountrySerializer(many=True)
    spoken_languages = SpokenLanguageSerializer(many=True)
    belongs_to_collection = CollectionSerializer(many=True)
    cast = CastSerializer(many=True)
    crew = CrewSerializer(many=True)
    backdrops = BackdropSerializer(many=True)
    posters = PosterSerializer(many=True)
    emoji = EmojiSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ('genre_rus_1', 'genre_rus_2', 'genre_rus_3', 'genre_rus_4', 'genre_rus_5', 'genre_rus_6', 'genre_rus_7',
        'genre_rus_8', 'genre_rus_9', 'genre_rus_10')

