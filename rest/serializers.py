""" serializers.py """
from rest_framework import serializers
from rest.models import Match, Player, Season, Shift, Shot, Team
from rest.helper import get_url

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    """ player serializer """
    class Meta:
        model = Player
        fields = ('player_id', 'first_name', 'last_name', 'jersey')

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    """ match serializer """
    season = serializers.ReadOnlyField(source='season.name')
    home_team = serializers.ReadOnlyField(source='home_team.team_name')
    visitor_team = serializers.ReadOnlyField(source='visitor_team.team_name')
    shots = serializers.SerializerMethodField('get_shots')
    shifts = serializers.SerializerMethodField('get_shifts')
    def get_shots(self, obj):
        """ get shots url """
        return '{0}/{1}={2}'.format(get_url(self.context['request'].META), 'shots?match_id', obj.match_id)
    def get_shifts(self, obj):
        """ get shifts url """
        return '{0}/{1}={2}'.format(get_url(self.context['request'].META), 'shifts?match_id', obj.match_id)
    class Meta:
        model = Match
        fields = ('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team', 'shifts', 'shots')

class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    """ season serializer """
    class Meta:
        model = Season
        fields = ('id', 'name', )

class ShiftSerializer(serializers.HyperlinkedModelSerializer):
    """ shot serializer """
    player = PlayerSerializer()
    match = MatchSerializer()
    class Meta:
        model = Shift
        fields = ('shift_id', 'match_id', 'match', 'player_id', 'player', 'starttime_sec', 'starttime_realtime', 'endtime_sec', 'endtime_realtime')

class ShotSerializer(serializers.HyperlinkedModelSerializer):
    """ shot serializer """
    player = PlayerSerializer()
    match = MatchSerializer()
    class Meta:
        model = Shot
        fields = ('shot_id', 'match_id', 'match', 'player_id', 'player', 'match_shot_resutl_id', 'timestamp', 'coordinate_x', 'coordinate_y', 'real_date', 'polygon', 'zone')

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """ team serializer """
    class Meta:
        model = Team
        fields = ('team_id', 'team_name', 'shortcut')
