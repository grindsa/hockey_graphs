""" views.py """
from django.db.models import Q
from django.conf import settings
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest.functions.matchday import matchdays_get
from rest.functions.matchstatistics import matchstatistics_get
from rest.functions.helper import logger_setup
from rest.version import __version__
from .serializers import MatchSerializer, PeriodeventSerializer, PlayerSerializer, ShiftSerializer, ShotSerializer, TeamSerializer
from .models import Match, Periodevent, Player, Shift, Shot, Team
import gettext

# initialize logger
DEBUG = settings.DEBUG

LOGGER = logger_setup(DEBUG)
LOGGER.info('starting hockeys_graphs rest api version %s ', __version__)
if DEBUG:
    LOGGER.debug('debug mode enabled')


en = gettext.translation('django', localedir='locale', languages=['en'])
de = gettext.translation('django', localedir='locale', languages=['de'])
en.install()
LCLANG = 'en'

def set_language(logger, request):
    """ select languate based on language id """
    if 'language' in request.GET:
        if request.GET['language'].lower() == 'de':
            logger.debug('switch language to "de"')
            de.install()
        else:
            logger.debug('switch language to "en"')
            en.install()

class SingleresultsSetPagination(PageNumberPagination):
    """ pagination for special serializers """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 20

class MatchStatisticsViewSet(viewsets.ViewSet):
    """ view for matchdays """

    def list(self, request):
        """ get a list of matchdays and matches per day """
        result = matchstatistics_get(LOGGER, request)
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def retrieve(self, request, pk=None):
        """ filter matches for a single matchday """
        set_language(LOGGER, request, LCLANG)


        result = matchstatistics_get(LOGGER, request, fkey='match', fvalue=pk)
        response = Response(result, status=status.HTTP_200_OK)
        return response

class MatchDayViewSet(viewsets.ViewSet):
    """ view for matchdays """

    def list(self, request):
        """ get a list of matchdays and matches per day """
        result = matchdays_get(LOGGER, request)
        response = Response(result, status=status.HTTP_200_OK)
        return response

    def retrieve(self, request, pk=None):
        """ filter matches for a single matchday """
        result = matchdays_get(LOGGER, request, fkey='date', fvalue=pk)
        response = Response(result, status=status.HTTP_200_OK)
        return response

# pylint: disable=R0901
class MatchViewSet(viewsets.ModelViewSet):
    """ viewset for matches """
    queryset = Match.objects.all().order_by('match_id')
    serializer_class = MatchSerializer
    http_method_names = ['get']

# pylint: disable=R0901
class PlayerViewSet(viewsets.ModelViewSet):
    """ viewset for players """
    queryset = Player.objects.all().order_by('player_id')
    serializer_class = PlayerSerializer
    http_method_names = ['get']

# pylint: disable=R0901
class PeriodeventViewSet(viewsets.ModelViewSet):
    """ viewset for periodevents """
    serializer_class = PeriodeventSerializer
    pagination_class = SingleresultsSetPagination
    http_method_names = ['get']
    def get_queryset(self):
        match_id = self.request.query_params.get('match_id', None)
        if match_id:
            queryset = Periodevent.objects.filter(match_id=match_id).order_by('match_id').values('period_event').distinct()
        else:
            queryset = Periodevent.objects.none()
        return queryset

    # pylint: disable=W0613
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.values_list('period_event', flat=True))

# pylint: disable=R0901
class ShiftViewSet(viewsets.ModelViewSet):
    """ viewset for shifts """
    serializer_class = ShiftSerializer
    pagination_class = SingleresultsSetPagination
    http_method_names = ['get']

    def get_queryset(self):
        match_id = self.request.query_params.get('match_id', None)
        if match_id:
            queryset = Shift.objects.filter(match_id=match_id).order_by('match_id').values('shift').distinct()
        else:
            queryset = Shift.objects.none()
        return queryset

    # pylint: disable=W0613
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.values_list('shift', flat=True))

# pylint: disable=R0901
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

# pylint: disable=R0901
class TeamViewSet(viewsets.ModelViewSet):
    """ viewset for teams """
    queryset = Team.objects.all().order_by('team_id')
    serializer_class = TeamSerializer
    http_method_names = ['get']
