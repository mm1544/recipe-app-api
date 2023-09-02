"""
URL mappings for the recipy app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

router = DefaultRouter()
# Registereing a viewset with/on router with name 'recipes'
# It will create a new endpoint 'api/recipes' and it will assign all the fdifferent \
# endpoints from our 'views.RecipeViewSet' to that endpoint.
# 'RecipeViewSet' will have auto-generated URLs depending on the functionality that \
# is enabled on the viewset. Because we use 'ModelViewSet', it is going to support \
# all the available methods for (CRUD) Create, Read, Update and Delete, which is \
# HTTP get, post, put and patch requests. It will create and registed all the \
# endpoints for each of these options (HTTP requests).
router.register('recipes', views.RecipeViewSet)

# Name that is used to identify when we are doing 'reverse' look-up of URLs.
app_name = 'recipe'

urlpatterns = [
    # Used to include URLs that are generated automatically by the router (all URLs \
    # that are available).
    path('', include(router.urls)),
    # Need to wire this up in the main urls.
]
