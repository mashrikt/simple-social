import factory
import pytest
from django.urls import reverse

from .factories import PostFactory
from ..models import Post, Reaction


class TestListPost:
    @pytest.fixture
    def url(self):
        return reverse('api:posts:list-create')

    def test_get_list_of_posts(self, auth_client, url, post, reaction):
        response = auth_client.get(url)
        assert response.status_code == 200
        data = response.data
        assert len(data['results']) == 1
        returned_post = data['results'][0]
        assert returned_post['id'] == post.id
        assert returned_post['text'] == post.text
        assert returned_post['reactions'][f'{reaction.type.lower()}s'] == 1

    def test_not_authenticated_user_cannot_get_list_of_posts(self, client, url, post):
        response = client.get(url)
        assert response.status_code == 403


class TestCreatePost:
    @pytest.fixture
    def url(self):
        return reverse('api:posts:list-create')

    @pytest.fixture
    def post_data(self):
        data = factory.build(dict, FACTORY_CLASS=PostFactory)
        del data['created_by']
        return data

    def test_user_create_post(self, auth_client, url, post_data, user):
        response = auth_client.post(url, post_data)
        assert response.status_code == 201
        returned = response.data
        created = Post.objects.get(id=returned['id'])
        assert created.text == returned['text'] == post_data['text']
        assert created.created_by == user


    def test_not_authenticated_user_cannot_create_post(self, client, url, post_data):
        response = client.post(url, post_data)
        assert response.status_code == 403


class TestRetrievePost:
    @pytest.fixture
    def url(self, post):
        return reverse('api:posts:retrieve-update-destroy', args=[post.id])

    def test_get_post(self, auth_client, url, post, reaction):
        response = auth_client.get(url)
        assert response.status_code == 200
        data = response.data
        assert data['id'] == post.id
        assert data['text'] == post.text
        assert data['reactions'][f'{reaction.type.lower()}s'] == 1

    def test_not_authenticated_user_cannot_get_post(self, client, url, post):
        response = client.get(url)
        assert response.status_code == 403


class TestUpdatePost:
    @pytest.fixture
    def url(self, post):
        return reverse('api:posts:retrieve-update-destroy', args=[post.id])

    @pytest.mark.parametrize('method', ['patch', 'put'])
    def test_update_post(self, auth_client, method, url, post):
        data = {'text': 'hello earth!'}
        response = getattr(auth_client, method)(url, data)
        assert response.status_code == 200
        data = response.data
        assert data['id'] == post.id
        assert data['text'] == 'hello earth!'

    def test_user_who_did_not_create_post_cant_update(self, other_client, url):
        response = other_client.put(url)
        assert response.status_code == 403


class TestDestroyPost:
    @pytest.fixture
    def url(self, post):
        return reverse('api:posts:retrieve-update-destroy', args=[post.id])

    def test_delete_post(self, auth_client, url):
        response = auth_client.delete(url)
        assert response.status_code == 204

    def test_user_who_did_not_create_post_cant_delete(self, other_client, url):
        response = other_client.delete(url)
        assert response.status_code == 403


class TestCreateReaction:
    @pytest.fixture
    def url(self, post):
        return reverse('api:posts:reactions-list-create', args=[post.id])

    def test_user_reaction(self, auth_client, url, post):
        data = {'type': 'LIKE'}
        response = auth_client.post(url, data)
        assert response.status_code == 201
        count = Reaction.objects.filter(post=post).count()
        assert count == 1

    def test_user_cannot_react_twice_on_the_same_post(self, auth_client, url, post, user):
        data = {'type': 'LIKE'}
        Reaction.objects.create(post=post, created_by=user, type='LIKE')
        response = auth_client.post(url, data)
        assert response.status_code == 400
        assert response.data['non_field_errors'][0] == 'User has already reacted to this post.'
        count = Reaction.objects.filter(post=post).count()
        assert count == 1

    def test_not_authenticated_user_cant_react(self, auth_client, url, post):
        data = {'type': 'LIKE'}
        response = auth_client.post(url, data)
        assert response.status_code == 201


class TestUpdateReaction:
    @pytest.fixture
    def url(self, post, reaction):
        return reverse('api:posts:reactions-retrieve-update-destroy', args=[post.id, reaction.id])

    @pytest.mark.parametrize('method', ['patch', 'put'])
    def test_update_reaction(self, auth_client, method, url):
        data = {'type': 'DISLIKE'}
        response = getattr(auth_client, method)(url, data)
        assert response.status_code == 200
        assert response.data['type'] == 'DISLIKE'

    def test_user_not_creator_of_reaction_cant_update(self, other_client, url):
        data = {'type': 'DISLIKE'}
        response = other_client.patch(url, data)
        assert response.status_code == 403


class TestDeleteReaction:
    @pytest.fixture
    def url(self, post, reaction):
        return reverse('api:posts:reactions-retrieve-update-destroy', args=[post.id, reaction.id])

    def test_delete_reaction(self, auth_client, url, post):
        post_id = post.id
        response = auth_client.delete(url)
        assert response.status_code == 204
        exists = Reaction.objects.filter(post_id=post_id).exists()
        assert exists == False

    def test_user_not_creator_of_reaction_cant_delete(self, other_client, url):
        response = other_client.delete(url)
        assert response.status_code == 403
