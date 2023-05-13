

from .views import *
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path(_(''), download_video, name='home'),
    path('download/<itag>', downloadvideo, name='download'),
    # path('details/',detailsFunction,name="details"),
    # path('download/',downloadFunction,name="download")
]
