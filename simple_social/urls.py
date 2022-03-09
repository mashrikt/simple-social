"""simple_social URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .socials.urls import posts_patterns
from .users.urls import auth_patterns


schema_view = get_schema_view(
   openapi.Info(
      title="Simple Social API",
      default_version='v1',
      description="Simple textual social network",
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


api_patterns = [
    path('auth/', include(arg=(auth_patterns, 'auth_patterns'), namespace='auth')),
    path('posts/', include(arg=(posts_patterns, 'posts_patterns'), namespace='posts')),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/', include(arg=(api_patterns, 'api_patterns'), namespace='api')),
]
