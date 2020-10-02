""" views.py """
from django.shortcuts import render
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import MatchSerializer, PeriodeventSerializer, PlayerSerializer, ShiftSerializer, ShotSerializer, TeamSerializer
from .models import Match, Periodevent, Player, Shift, Shot, Team
from rest_framework.pagination import PageNumberPagination

class SingleresultsSetPagination(PageNumberPagination):
    """ pagination for special serializers """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class MatchViewSet(viewsets.ModelViewSet):
    """ viewset for matches """
    queryset = Match.objects.all().order_by('match_id')
    serializer_class = MatchSerializer
    http_method_names = ['get']

class PlayerViewSet(viewsets.ModelViewSet):
    """ viewset for players """
    queryset = Player.objects.all().order_by('player_id')
    serializer_class = PlayerSerializer
    http_method_names = ['get']

class PeriodeventViewSet(viewsets.ModelViewSet):
    """ viewset for periodevents """
    serializer_class = PeriodeventSerializer
    pagination_class = SingleresultsSetPagination
    http_method_names = ['get']
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
    """ viewset for shifts """
    serializer_class = ShiftSerializer
    pagination_class = SingleresultsSetPagination
    http_method_names = ['get']
    def get_queryset(self):
        match_id = self.request.query_params.get('match_id', None)
        player_id = self.request.query_params.get('player_id', None)
        if match_id:
            queryset = Shift.objects.filter(match_id=match_id).order_by('match_id').values('shift').distinct();
        else:
            queryset =  Shift.objects.none();
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.values_list('shift', flat=True))

class ShotViewSet(viewsets.ModelViewSet):
    """ viewset for shots """
    serializer_class = ShotSerializer
    http_method_names = ['get']
    def get_queryset(self):
        match_id = self.request.query_params.get('match_id', None)
        player_id = self.request.query_params.get('player_id', None)
        if match_id and player_id:
            queryset = Shot.objects.filter(Q(match_id=match_id), Q(player_id=player_id)).order_by('shot_id')
        elif match_id:
            queryset = Shot.objects.filter(match_id=match_id).order_by('shot_id')
        elif player_id:
            queryset = Shot.objects.filter(player_id=player_id).order_by('shot_id')
        else:
            queryset = Shot.objects.all().order_by('shot_id')

        return queryset

class TeamViewSet(viewsets.ModelViewSet):
    """ viewset for teams """
    queryset = Team.objects.all().order_by('team_id')
    serializer_class = TeamSerializer
    http_method_names = ['get']
