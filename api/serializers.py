import logging
import os
import time

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework import status
from rest_framework.relations import SlugRelatedField
from rest_framework.serializers import SlugField, ValidationError
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model
# from rest_framework.exceptions import APIException

from .models import Post, Comment, Group, Follow


User = get_user_model()

FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
log = logging.getLogger('TELEGRAM_BOT_APP')


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('user', 'following', )
        read_only_fields = ('user', )
        model = Follow
    
    def to_representation(self, instance):
        # log.info(f'to_representation(instance): {instance}')
        # log.info(f'to_representation(type - instance): {type(instance)}')
        # data = super(FollowSerializer, self).to_representation(instance)
        # log.info(f'to_representation(data): {data}')
        # log.info(f'to_representation(type - data): {type(data)}')
        return {
            'user': instance.user.username,
            'following': instance.following.username
        }

    def to_internal_value(self, data):

        # log.info(f'to_internal_value(user): {data.get("user")}')

        following = data.get('following')
        # log.info(f'to_internal_value(following): {following}')

        if not following:
            raise ValidationError({
                'following': 'This field is required.'
            })

        author = User.objects.filter(username=following).first()
        if not author:
            raise ValidationError({
                'following': 'There is no user with this username.'
            })

        return {
            'following': author,
        }

    def validate(self, data):
        user = self.context['request'].user
        following = data.get('following')

        log.info(f'validate (user): {user}')
        log.info(f'validate (following): {following}')

        if Follow.objects.filter(user=user, following=following).count() > 0:
            raise ValidationError(
                detail='this user-following pair already exists',
                code=status.HTTP_400_BAD_REQUEST
            )

        if user == following:
            raise ValidationError(
                detail='user and following shall be different',
                code=status.HTTP_400_BAD_REQUEST
            )

        return {'following': following}

    def create(self, validated_data):
        user = validated_data.get('user')
        # log.info(f'create (USER): {user}')

        following = validated_data.get('following')
        # log.info(f'create(AUTHOR): {author}')

        return Follow.objects.create(user=user, following=following)
            # log.info(f'create(follow): {follow}')
            # log.info(f'create(follow - type): {type(follow)}')
            # log.info(f'create(follow.user): {follow.user}')
            # log.info(f'create(type - follow.user): {type(follow.user)}')
            # log.info(f'create(follow.author): {follow.author}')
            # log.info(f'create(type - follow.author): {type(follow.author)}')


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        read_only_fields = ('post',)
        model = Comment
