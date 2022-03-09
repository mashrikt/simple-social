import pytest

from .factories import PostFactory, ReactionFactory


@pytest.fixture
def post(user):
    return PostFactory(created_by=user)


@pytest.fixture
def reaction(post, user):
    return ReactionFactory(post=post, created_by=user)
