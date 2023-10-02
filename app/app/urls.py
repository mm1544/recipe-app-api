"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    # Adding URL here because it is JUST A TEST!!
    path('api/healt-check/', core_views.health_check, name='health-check'),
    # SpectacularAPIView will generate the schema file \
    # needed for our project.
    path('api/schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'api/docs/',
        # rl_name='api-schema' -> Telling what schema \
        # to use when loading Swagger
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs',
    ),
    path('api/user/', include('user.urls')),
    path('api/recipe/', include('recipe.urls')),
]

# If we are running in Debug mode. It will happen when we are running \
# on local machine on development server.
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        # Allowing to server Media files. Dj dev server by default \
        # doesn't serve these files.
        document_root=settings.MEDIA_ROOT,
    )
