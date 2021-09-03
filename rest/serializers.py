""" serializers.py """
from django.conf import settings
from rest_framework import serializers
from rest.models import Match, Periodevent, Player, Season, Shift, Shot, Team
from rest.functions.helper import url_build, logger_setup
from rest.functions.match import matchstats_get

# initialize logger
DEBUG = settings.DEBUG
LOGGER = logger_setup(DEBUG)

class PlayerSerializer(serializers.HyperlinkedModelSerializer):
    """ player serializer """
    id = serializers.SerializerMethodField('get_id')
    name = serializers.SerializerMethodField('get_name')
    def get_name(self, obj):
        """ get name and jersey """
        if self.context:
            return '{0} {1}'.format(obj.first_name, obj.last_name)
    def get_id(self, obj):
        """ get id """
        if self.context:
            return obj.player_id
    class Meta:
        model = Player
        # fields = ('player_id', 'first_name', 'last_name', 'jersey')
        fields = ('id', 'name')

class MatchSerializer(serializers.HyperlinkedModelSerializer):
    """ match serializer """
    season = serializers.ReadOnlyField(source='season.name')
    home_team = serializers.ReadOnlyField(source='home_team.team_name')
    visitor_team = serializers.ReadOnlyField(source='visitor_team.team_name')
    events = serializers.SerializerMethodField('get_events')
    shots = serializers.SerializerMethodField('get_shots')
    shifts = serializers.SerializerMethodField('get_shifts')
    stats = serializers.SerializerMethodField('get_stats')
    # shrink data in overview
    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(MatchSerializer, self).__init__(*args, **kwargs)
        if len(args) > 0 and isinstance(args[0], list):
            self.fields.pop('events')
            self.fields.pop('shifts')
            self.fields.pop('shots')
    def get_events(self, obj):
        """ get events url """
        if self.context:
            return '{0}/api/v1/{1}={2}'.format(url_build(self.context['request'].META), 'events?match_id', obj.match_id)
    def get_shots(self, obj):
        """ get shots url """
        if self.context:
            return '{0}/api/v1/{1}={2}'.format(url_build(self.context['request'].META), 'shots?match_id', obj.match_id)
    def get_shifts(self, obj):
        """ get shifts url """
        if self.context:
            return '{0}/api/v1/{1}={2}'.format(url_build(self.context['request'].META), 'shifts?match_id', obj.match_id)
    def get_stats(self, obj):
        """ get stats """
        if self.context:
            return matchstats_get(LOGGER, obj.match_id)

    class Meta:
        model = Match
        fields = ('match_id', 'season', 'date', 'date_uts', 'home_team', 'visitor_team', 'result', 'shifts', 'shots', 'events', 'stats')

class PeriodeventSerializer(serializers.HyperlinkedModelSerializer):
    """ shot Periodevent """
    # match = serializers.ReadOnlyField(source='match.match_id')
    class Meta:
        model = Periodevent
        fields = ('period_event', )

class SeasonSerializer(serializers.HyperlinkedModelSerializer):
    """ season serializer """
    class Meta:
        model = Season
        fields = ('id', 'name', 'shortcut')

class ShiftSerializer(serializers.HyperlinkedModelSerializer):
    """ shot serializer """
    # match = serializers.ReadOnlyField(source='match.match_id')
    class Meta:
        model = Shift
        fields = ('shift', )

class ShotSerializer(serializers.HyperlinkedModelSerializer):
    """ shot serializer """
    player = PlayerSerializer()
    match = serializers.ReadOnlyField(source='match.match_id')
    class Meta:
        model = Shot
        fields = ('shot_id', 'match_id', 'match', 'player_id', 'player', 'match_shot_resutl_id', 'timestamp', 'coordinate_x', 'coordinate_y', 'real_date', 'polygon', 'zone')

class TeamSerializer(serializers.HyperlinkedModelSerializer):
    """ team serializer """
    class Meta:
        model = Team
        fields = ('team_id', 'team_name', 'shortcut')
