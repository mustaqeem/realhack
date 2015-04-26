from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import include
from . import views

urlpatterns = patterns('',
    url(r'^keyword-suggestion/$', views.KeywordSuggestion.as_view()),
    url(r'^get-heatmap-data/$', views.HeatMapData.as_view()),
    url(r'^get-listing-data/$', views.Listings.as_view())
)

urlpatterns = format_suffix_patterns(urlpatterns)
