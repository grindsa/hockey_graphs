""" views.py """
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MatchSerializer, PlayerSerializer, ShotSerializer, TeamSerializer
from .models import Match, Player, Shot, Team

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('match_id')
    serializer_class = MatchSerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all().order_by('player_id')
    serializer_class = PlayerSerializer

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
