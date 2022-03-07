from django.db import IntegrityError
from dj_rest_auth.serializers import UserDetailsSerializer
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, SerializerMethodField, UniqueTogetherValidator

from .models import Post, Reaction


class PostSerializer(ModelSerializer):
    created_by = UserDetailsSerializer(read_only=True)
    reactions = SerializerMethodField()

    class Meta:
        model = Post
        fields = ('id', 'text', 'created_at', 'created_by', 'reactions')

    def get_reactions(self, obj):
        reaction_count = dict(obj.get_reaction_count)
        return {
            'likes': reaction_count.get(Reaction.LIKE, 0),
            'dislikes': reaction_count.get(Reaction.DISLIKE, 0),
        }

class ReactionSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'type')

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except IntegrityError:
            raise ValidationError({"non_field_errors ": ["User has already reacted to this post."]})

class ReactionDetailSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = ('id', 'type', 'created_by')
