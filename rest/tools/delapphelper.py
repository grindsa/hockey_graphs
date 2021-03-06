# -*- coding: utf-8 -*-
""" delapphelper """
import sys
import os
from datetime import datetime
import requests
import urllib3
from rest.functions.helper import config_load, logger_setup

from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def print_debug(debug, text):
    """ little helper to print debug messages """
    if debug:
        print('{0}: {1}'.format(datetime.now(), text))

class DelAppHelper():
    """ main class to access the PA REST API """
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    debug = None
    os_ = 'android'
    logger = None
    deviceid = None
    tournamentid = None
    base_url = None
    mobile_api = None
    del_api = None
    shift_name = None

    def __init__(self, debug=False, deviceid='bada55bada55666'):
        self.debug = debug
        self.deviceid = deviceid
        self.logger = logger_setup(debug)

    def __enter__(self):
        """ Makes Stirpahelper a Context Manager
        with DelAppHelper(....) as del_app_helper:
            print (...) """
        self._config_load()
        return self

    def __exit__(self, *args):
        """ Close the connection at the end of the context """
        # self.logout()
        pass

    def _config_load(self):
        """" load config from file """
        self.logger.debug('_config_load()')
        config_dic = config_load(cfg_file=os.path.dirname(__file__)+'/'+'hockeygraphs.cfg')
        if 'Tools' in config_dic:
            if 'base_url' in config_dic['Tools']:
                self.base_url = config_dic['Tools']['base_url']
            if 'mobile_api' in config_dic['Tools']:
                self.mobile_api = config_dic['Tools']['mobile_api']
            if 'del_api' in config_dic['Tools']:
                self.del_api = config_dic['Tools']['del_api']
            if 'Shifts' in config_dic and 'shift_name' in config_dic['Shifts']:
                self.shift_name = config_dic['Shifts']['shift_name']

        self.logger.debug('_config_load() ended.')

    def api_post(self, url, data):
        """ generic wrapper for an API post call """
        self.logger.debug('DelAppHelper.api_post()\n')
        data['os'] = self.os_
        api_response = requests.post(url=url, data=data, headers=self.headers, verify=False)
        if api_response.ok:
            json_dic = api_response.json()
            return json_dic
        else:
            print(api_response.raise_for_status())
            return None

    def gamesituations_get(self, game_id):
        """ get game situations """
        self.logger.debug('DelAppHelper.gamesituations_get({0})\n'.format(game_id))
        data = {'requestName': 'gameSituations',
                'gameNumber': game_id,
                'tournamentId': self.tournamentid,
                'lastUpdate': 0}
        return self.api_post(self.mobile_api, data)

    def game_filter(self, date_, team):
        """ filter match based on time and team name """
        self.logger.debug('DelAppHelper.match_filter({0}, {1})\n'.format(date_, team))
        game_dic = self.games_get()

        game_details = {}
        for game in game_dic:
            if game['dateTime'] == date_:
                if team in (game['guestTeam'], game['homeTeam']):
                    game_details = game
                    break

        return game_details

    def gameheader_get(self, match_id):
        """ get periodevents from del.org """
        self.logger.debug('DelAppHelper.gameheader_get({0})\n'.format(match_id))

        url = '{0}/matches/{1}/game-header.json'.format(self.base_url, match_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def gameresult_get(self, game_id):
        """ get games """
        self.logger.debug('DelAppHelper.gameresult_get()\n')
        data = {'requestName': 'gameResults',
                'gameNumber': game_id,
                'tournamentId': self.tournamentid,
                'lastUpdate': 0}
        return self.api_post(self.mobile_api, data)

    def games_get(self, tournamentid=None):
        """ get games """
        self.logger.debug('DelAppHelper.games_get({0}) via mobile_api\n'.format(tournamentid))

        if not tournamentid:
            tournamentid = self.tournamentid

        data = {'requestName': 'games',
                'deviceId': self.deviceid,
                'tournamentId': tournamentid,
                'lastUpdate': 0}
        return self.api_post(self.mobile_api, data)

    def lineup_get(self, game_id):
        """ get lineup """
        self.logger.debug('DelAppHelper.linup_get()\n')
        data = {'requestName': 'gameLineup',
                'tournamentId': self.tournamentid,
                'lastUpdate': 0,
                'gameNumber': game_id}
        # Positions
        # 3 - leftwing
        # 4 - center
        # 5 - rigtwing
        # 1 - rdefense
        # 2 - defense

        return self.api_post(self.mobile_api, data)

    def lineup_dict(self, game_id, home_match):
        """ get lineup """
        self.logger.debug('DelAppHelper.linup_get()\n')

        # Positions
        # 3 - leftwing
        # 4 - center
        # 5 - rigtwing
        # 1 - rdefense
        # 2 - defense

        result = self.lineup_get(game_id)

        lineup_dic = {}
        for player in result:
            if player['lineNumber'] not in lineup_dic:
                lineup_dic[player['lineNumber']] = {}

            if home_match:
                if player['homePlayerNumber'] != 0:
                    lineup_dic[player['lineNumber']][player['linePosition']] = '{0} ({1})'.format(player['homePlayerName'], player['homePlayerNumber'])
            else:
                if player['guestPlayerNumber'] != 0:
                    lineup_dic[player['lineNumber']][player['linePosition']] = '{0} ({1})'.format(player['guestPlayerName'], player['guestPlayerNumber'])

        return (lineup_dic, result)

    def line_get(self, line_dic, headline):
        """ line get """
        self.logger.debug('DelAppHelper.line_get()\n')
        line = '*{0}*\n'.format(headline)

        if 4 in line_dic:
            line = '{0}{1}\n'.format(line, line_dic[4])
        if 3 in line_dic:
            line = '{0}{1}\n'.format(line, line_dic[3])
        if 5 in line_dic:
            line = '{0}{1}\n'.format(line, line_dic[5])
        if 1 in line_dic:
            line = '{0}{1}\n'.format(line, line_dic[1])
        if 2 in line_dic:
            line = '{0}{1}\n'.format(line, line_dic[2])
        return line

    def lineup_format(self, game_id, home_match, match_id, store_lineup=False):
        """ get format """
        self.logger.debug('DelAppHelper.linup_format()\n')
        (lineup_dic, raw_json) = self.lineup_dict(game_id, home_match)

        lineup = ''
        data_dic = {}
        if 0 in lineup_dic:
            if lineup_dic[0]:
                line = self.line_get(lineup_dic[0], 'Goalies')
                lineup = '{0}{1}\n'.format(lineup, line)
        if 1 in lineup_dic:
            if lineup_dic[1]:
                line = self.line_get(lineup_dic[1], '1. Reihe')
                lineup = '{0}{1}\n'.format(lineup, line)
                data_dic['r1'] = line
        if 2 in lineup_dic:
            if lineup_dic[2]:
                line = self.line_get(lineup_dic[2], '2. Reihe')
                lineup = '{0}{1}\n'.format(lineup, line)
                data_dic['r2'] = line
        if 3 in lineup_dic:
            if lineup_dic[3]:
                line = self.line_get(lineup_dic[3], '3. Reihe')
                lineup = '{0}{1}\n'.format(lineup, line)
                data_dic['r3'] = line
        if 4 in lineup_dic:
            if lineup_dic[4]:
                line = self.line_get(lineup_dic[4], '4. Reihe')
                lineup = '{0}{1}\n'.format(lineup, line)
                data_dic['r4'] = line
        if 5 in lineup_dic:
            if lineup_dic[5]:
                line = self.line_get(lineup_dic[5], '5. Reihe')
                lineup = '{0}{1}\n'.format(lineup, line)
                data_dic['r5'] = line

        if lineup and store_lineup:
            data_dic['lineup'] = lineup
            data_dic['raw_json'] = raw_json
            self.lineup_store(match_id, data_dic)
            lineup = 'Anbei die Aufstellung für das heutige Spiel:\n\n{0}'.format(lineup)

        return lineup

    def lineup_store(self, match_id, data_dic):
        """ get format """
        self.logger.debug('DelAppHelper.lineup_store()\n')
        # store in db
        data_dic['match_id'] = match_id
        obj, _created = Lineup.objects.update_or_create(match_id=match_id, defaults=data_dic)
        obj.save()

    def myteam_get(self, team):
        """ get games """
        self.logger.debug('DelAppHelper.myteam_get({0})\n'.format(team))
        data = {'requestName': 'myTeam',
                'deviceId': self.deviceid,
                'tournamentId': self.tournamentid,
                'noc': team,
                'lastUpdate': 1}
        return self.api_post(self.mobile_api, data)

    def periodevents_get(self, match_id):
        """ get periodevents from del.org """
        self.logger.debug('DelAppHelper.periodevents_get({0}) from del.org\n'.format(match_id))

        url = '{0}/matches/{1}/period-events.json'.format(self.base_url, match_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def playerstats_get(self, match_id, home):
        """ get playerstats_get from del.org """
        self.logger.debug('DelAppHelper.playerstats_get({0}:{1})\n'.format(match_id, home))

        if home:
            url = '{0}/matches/{1}/player-stats-home.json'.format(self.base_url, match_id)
        else:
            url = '{0}/matches/{1}/player-stats-guest.json'.format(self.base_url, match_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def playofftree_get(self, year_, league_id=3):
        """ get playoff tree """
        self.logger.debug('DelAppHelper.playofftree_get({0}:{1})\n'.format(year_, league_id))
        url = '{0}/league-playoffs/{1}/{2}.json'.format(self.del_api, year_, league_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def reflist_format(self, game_id, match_id):
        """ get refs """
        self.logger.debug('DelAppHelper.reflist_format()\n')
        (ref_list, ref_dic) = self.reflist_get(game_id)


        if 'Ref1' in ref_dic and 'Ref2' in ref_dic:
            self.reflist_store(match_id, [ref_dic['Ref1'], ref_dic['Ref2']])

        if ref_list:
            ref_ = 'Anbei die Schiedsrichter für das heutige Spiel:\n\n'
            for referee in ref_list:
                ref_ = '{0}{1}\n'.format(ref_, referee)
            return ref_
        else:
            return None

    def ref_create(self, refname):
        """ create new ref in database """
        self.logger.debug('DelAppHelper.ref_create({0})\n'.format(refname))
        obj = Referee(name=refname)
        obj.save()
        return obj.id

    def reflist_store(self, match_id, ref_list):
        """ get format """
        self.logger.debug('DelAppHelper.reflist_store()\n')

        # list of referees
        referee_list = Referee.objects.values('id', 'name')

        ref_id_list = []
        # ref_name_list = []
        for refl in ref_list:
            found_ref = False
            for ref in referee_list:
                # search referre list for ids
                (_sinin, lname) = refl.split(' ', 1)
                if lname.lower() in ref['name'].lower():
                    found_ref = True
                    self.logger.debug('{0} {1} {2}'.format(lname, ref['id'], ref['name']))
                    ref_id_list.append(ref['id'])
                    # ref_name_list.append(ref['name'])
                    break
            if not found_ref:
                # new ref to be created
                id_ = self.ref_create(refl)
                ref_id_list.append(id_)

        if len(ref_id_list) == 2:
            # update database
            data_dic = {
                'match_id' : match_id,
                'r1_id'    : ref_id_list[0],
                'r2_id'    : ref_id_list[1],
            }
            # print('save to db')
            obj, _created = Refpermatch.objects.update_or_create(match_id=match_id, defaults=data_dic)
            obj.save()

    def reflist_get(self, game_id):
        """ get refs """
        self.logger.debug('DelAppHelper.reflist_get()\n')
        data = {'requestName': 'gameOfficials',
                'tournamentId': self.tournamentid,
                'lastUpdate': 0,
                'gameNumber': game_id}
        result = self.api_post(self.mobile_api, data)
        tmp_dic = {}
        if result:
            for ref in result:
                tmp_dic[ref['officialPosition']] = '{0} {1}'.format(ref['officialGivenName'], ref['officialFamilyName'])

        ref_list = []
        if 'Ref1' in tmp_dic:
            ref_list.append(tmp_dic['Ref1'])
        if 'Ref2' in tmp_dic:
            ref_list.append(tmp_dic['Ref2'])
        if 'Lin1' in tmp_dic:
            ref_list.append(tmp_dic['Lin1'])
        if 'Lin2' in tmp_dic:
            ref_list.append(tmp_dic['Lin2'])

        return (ref_list, tmp_dic)

    def roster_get(self, match_id):
        """ get match statistics per player """
        self.logger.debug('DelAppHelper.roster_get({0}) from del.org\n'.format(match_id))
        url = '{0}/matches/{1}/roster.json'.format(self.base_url, match_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def scorers_get(self, match_id):
        """ get match statistics per player """
        self.logger.debug('DelAppHelper.scorers_get({0})\n'.format(match_id))
        url = '{0}/matches/{1}/top-scorers.json'.format(self.base_url, match_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def shifts_get(self, match_id):
        """ get shifts from DEL api """
        self.logger.debug('DelAppHelper.shifts_get({0})\n'.format(match_id))
        url = '{0}/matches/{1}/{2}'.format(self.del_api, match_id, self.shift_name)
        return requests.get(url, headers=self.headers, verify=False).json()

    def shots_get(self, match_id):
        """ get shots from del.org """
        self.logger.debug('DelAppHelper.periodevents_get({0})\n'.format(match_id))
        url = '{0}/visualization/shots/{1}.json'.format(self.base_url, match_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def teamplayers_get(self, season_name, team_id=3, league_id=1):
        """ get playerinformation per team via rest """
        # 1 - for DEL Regular season
        # 3 - for DEL Playoffs
        # 4 - for Magenta Cup
        self.logger.debug('DelAppHelper.teamplayers_get({0}:{1})\n'.format(season_name, team_id))
        url = '{0}/league-team-stats/{1}/{2}/{3}.json'.format(self.del_api, season_name, league_id, team_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def teammatches_get(self, season_name, team_id=3, league_id=1):
        """ get matches for a certain team league_id - 1 regular, 3 playoff """
        self.logger.debug('DelAppHelper.teammatches_get({0}:{1}:{2})\n'.format(season_name, team_id, league_id))
        url = '{0}/league-team-matches/{1}/{2}/{3}.json'.format(self.del_api, season_name, league_id, team_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def teammembers_get(self, team_name):
        """ get data from all players of a team """
        self.logger.debug('DelAppHelper.teammembers_get({0})\n'.format(team_name))
        data = {'requestName': 'teamMembers',
                'tournamentId': self.tournamentid,
                'noc': team_name,
                'lastUpdate': 0}
        return self.api_post(self.mobile_api, data)

    def teamstats_get(self, match_id, home):
        """ get teamstats_get from del.org """
        self.logger.debug('DelAppHelper.teamstats_get({0}:{1})\n'.format(match_id, home))
        if home:
            url = '{0}/matches/{1}/team-stats-home.json'.format(self.base_url, match_id)
        else:
            url = '{0}/matches/{1}/team-stats-guest.json'.format(self.base_url, match_id)
        return requests.get(url, headers=self.headers, verify=False).json()

    def teamstandings_get(self):
        """ get games """
        self.logger.debug('DelAppHelper.teamStandings_get()\n')
        data = {'requestName': 'teamStandings',
                'tournamentId': self.tournamentid,
                'lastUpdate': 0}
        return self.api_post(self.mobile_api, data)

    def tournamentid_get(self):
        """ get tournament id """
        self.logger.debug('DelAppHelper.tournamentid_get() via mobile_api\n')
        data = {'requestName': 'tournamentList', 'lastUpdate': 0}
        result = self.api_post(self.mobile_api, data)
        if result:
            if 'tournamentID' in result[-1]:
                self.tournamentid = result[-1]['tournamentID']
        self.logger.debug('DelAppHelper.tournamentid_get() ended with: {}\n'.format(self.tournamentid))
        return result
