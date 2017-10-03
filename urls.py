
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns

from .views import *


urlpatterns = i18n_patterns(
    url("^overview$", OverView.as_view()),
)