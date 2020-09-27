""" serializers.py """
from rest_framework import serializers
from rest.models import Match, Team, Season

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Team
        fields = ('team_id', 'team_name')

class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Season
        fields = ('id', 'name', )

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    # season = SeasonSerializer()
    # home_team = TeamSerializer()
    # visitor_team = TeamSerializer()
    season = serializers.ReadOnlyField(source='season.name')
    home_team = serializers.ReadOnlyField(source='home_team.team_name')
    visitor_team = serializers.ReadOnlyField(source='visitor_team.team_name')
    class Meta:
        model = Match
        fields = ('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team')
