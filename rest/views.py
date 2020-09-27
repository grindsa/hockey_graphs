""" views.py """
from django.shortcuts import render
from rest_framework import viewsets
from .serializers import MatchSerializer
from .models import Match

class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all().order_by('match_id')
    serializer_class = MatchSerializer
