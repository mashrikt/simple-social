from factory import Faker, SubFactory, fuzzy
from factory.django import DjangoModelFactory

from ..models import Post, Reaction
from ...users.tests.factories import UserFactory


class PostFactory(DjangoModelFactory):
    text = Faker('text')
    created_by = SubFactory(UserFactory)

    class Meta:
        model = Post


class ReactionFactory(DjangoModelFactory):
    post = SubFactory(PostFactory)
    type = fuzzy.FuzzyChoice(Reaction.REACT_CHOICES, getter=lambda c: c[0])
    created_by = SubFactory(UserFactory)

    class Meta:
        model = Reaction
