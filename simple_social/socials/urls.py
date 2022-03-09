from django.urls import path

from .views import PostListCreateView, PostRetrieveUpdateDestroyView, ReactionListCreateView, ReactionRetrieveUpdateDestroyView


posts_patterns = [
    path('', PostListCreateView.as_view(), name='list-create'),
    path('<pk>/', PostRetrieveUpdateDestroyView.as_view(), name='retrieve-update-destroy'),
    path('<post_id>/reactions/', ReactionListCreateView.as_view(), name='reactions-list-create'),
    path('<post_id>/reactions/<pk>/', ReactionRetrieveUpdateDestroyView.as_view(),
        name='reactions-retrieve-update-destroy'),
]
