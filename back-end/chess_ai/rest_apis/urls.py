from django.urls import re_path

from .views import (postData)

urlpatterns = [
    re_path(r'^postdata', postData)
]