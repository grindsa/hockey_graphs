from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'events', views.PeriodeventViewSet, basename='Periodevent')
router.register(r'matches', views.MatchViewSet)
router.register(r'player', views.PlayerViewSet)
router.register(r'shifts', views.ShiftViewSet, basename='Shift')
router.register(r'shots', views.ShotViewSet)
router.register(r'teams', views.TeamViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
]
