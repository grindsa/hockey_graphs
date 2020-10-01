""" views.py """
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import MatchSerializer, PeriodeventSerializer, PlayerSerializer, ShiftSerializer, ShotSerializer, TeamSerializer
from .models import Match, Periodevent, Player, Shift, Shot, Team
from rest_framework.pagination import PageNumberPagination

class SmallresultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 20

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('match_id')
    serializer_class = MatchSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('player_id')
    serializer_class = PlayerSerializer

class PeriodeventViewSet(viewsets.ModelViewSet):
    serializer_class = PeriodeventSerializer
    pagination_class = SmallresultsSetPagination
    def get_queryset(self):
        match_id = self.request.query_params.get('match_id', None)
        if match_id:
            queryset = Periodevent.objects.filter(match_id=match_id).order_by('match_id').values('period_event').distinct();
        else:
            queryset =  Periodevent.objects.none();
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.values_list('period_event', flat=True))

class ShiftViewSet(viewsets.ModelViewSet):
    serializer_class = ShiftSerializer
    pagination_class = SmallresultsSetPagination
    def get_queryset(self):
        match_id = self.request.query_params.get('match_id', None)
        if match_id:
            queryset = Shift.objects.filter(match_id=match_id).order_by('match_id').values('shift').distinct();
        else:
            queryset =  Shift.objects.none();
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.values_list('shift', flat=True))

class ShotViewSet(viewsets.ModelViewSet):
    queryset = Shot.objects.all().order_by('shot_id')
    serializer_class = ShotSerializer

    def get_queryset(self):
        queryset = self.queryset
        match_id = self.request.query_params.get('match_id', None)
        if match_id:
            queryset = queryset.filter(match_id=match_id)
        return queryset

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('team_id')
    serializer_class = TeamSerializer
