""" urls.py """
from django.urls import include, path
from django.conf.urls import url
from rest_framework import routers
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from . import views

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'events', views.PeriodeventViewSet, basename='Periodevent')
router.register(r'matches', views.MatchViewSet)
router.register(r'matchdays', views.MatchDayViewSet, basename='matchdays')
router.register(r'matchstatistics', views.MatchStatisticsViewSet, basename='matchstatistics')
router.register(r'teamcomparison', views.TeamComparisonViewSet, basename='teamcomparison')
router.register(r'players', views.PlayerperSeasonViewSet, basename='PlayerperSeason')
router.register(r'playerstatistics', views.PlayerStatisticsViewSet, basename='playerstatistics')
# router.register(r'shifts', views.ShiftViewSet, basename='Shift')
router.register(r'seasons', views.SeasonViewSet)
# router.register(r'shots', views.ShotViewSet, basename='Shot')
router.register(r'teams', views.TeamViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    url(r'^playerstatistics/(?P<season_pk>\d+)/(?P<player_pk>\d+)/?$', views.PlayerStatisticsViewSet.as_view({'get': 'list'}), name='playerstatistics')
    # url(r'^matchdays/(?P<resource_id>\d+)[/]?$', views.MatchDayViewSet.as_view(), name='MatchDayViewSet'),
    # url(r'^matchdays[/]?$', views.MatchDayViewSet.as_view(), name='MatchDayViewSet'),
    #url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    # url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
