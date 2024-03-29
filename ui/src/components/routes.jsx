import React from 'react';
import { MatchDayList } from '../components/matchday';
import { TeamComparison } from '../components/teamcomparison';
import { Playerstatistic } from '../components/playerstatistic';
import { Dsgvo } from '../components/dsgvo';

function tc_route(endpoint, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, stat){
  // update season and return TeamComparison route
  season = parseInt(season)
  if (season && selectedSeason && season && season !== selectedSeason) {
    setSelectedSeason(season)
  }
  if(selectedStat != 1){
    // checkge stat in upper bar if required
    changeStat(1)
  }
  return(
    <TeamComparison  teamcomparison={ endpoint } language={ language } season={ selectedSeason } stat={stat} />
  )
}

function mdl_route(ep_matchdays, ep_matchstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, matchid, stat){
  // update season and return MatchDayList route
  season = parseInt(season)
  if (matchid){
    // convert matchid to int for comparison in matchday.jsx
    matchid = parseInt(matchid)
  }
  if(stat){
    // covert stat to integer for comparison in matchstatistics.jsx
    stat = parseInt(stat)
  }
  if (season && selectedSeason && season && season !== selectedSeason) {
    setSelectedSeason(season)
  }
  if(selectedStat != 0){
    // checkge stat in upper bar if required
    changeStat(0)
  }
  return(
    <MatchDayList matchdays={ep_matchdays} matchstatistics={ep_matchstatistics} language={language} season={season} matchid={matchid} stat={stat}/>
  )
}

function ps_route(pl_endpoint, pls_endpoint, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, player, stat){
  // update season and return TeamComparison route
  season = parseInt(season)
  if (season && selectedSeason && season && season !== selectedSeason) {
    setSelectedSeason(season)
  }
  if(selectedStat != 2){
    // checkge stat in upper bar if required
    changeStat(2)
  }
  return(
    <Playerstatistic players={ pl_endpoint } playerstatistics={ pls_endpoint } language={ language } season={ selectedSeason } stat={stat} player_id={player}/>
  )
}

export const Routes = (endpoints, language, selectedSeason, setSelectedSeason, selectedStat, changeStat) => {
    return ({
      '/': () => <MatchDayList matchdays={endpoints.matchdays} matchstatistics={endpoints.matchstatistics} language={language} season={selectedSeason} />,
      '/dsgvo': () => <Dsgvo />,

      // just the path
      '/matchstatistics': () => <MatchDayList matchdays={endpoints.matchdays} matchstatistics={endpoints.matchstatistics} language={language} season={selectedSeason} />,
      // just the season
      '/matchstatistics/:season': ({season}) => mdl_route(endpoints.matchdays, endpoints.matchstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, null, null),
      '/matchstatistics/:season/': ({season}) => mdl_route(endpoints.matchdays, endpoints.matchstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, null, null),
      // season and match
      '/matchstatistics/:season/:matchid': ({season, matchid}) => mdl_route(endpoints.matchdays, endpoints.matchstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, matchid, null),
      '/matchstatistics/:season/:matchid/': ({season, matchid}) => mdl_route(endpoints.matchdays, endpoints.matchstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, matchid, null),
      // season, match and stat
      '/matchstatistics/:season/:matchid/:stat': ({season, matchid, stat}) => mdl_route(endpoints.matchdays, endpoints.matchstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, matchid, stat),
      '/matchstatistics/:season/:matchid/:stat/': ({season, matchid, stat}) => mdl_route(endpoints.matchdays, endpoints.matchstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, matchid, stat),

      // just the path
      '/teamcomparison': () => tc_route(endpoints.teamcomparison, language, selectedSeason, selectedSeason, setSelectedSeason, selectedStat, changeStat, "1"),
      // just the season
      '/teamcomparison/:season': ({season}) => tc_route(endpoints.teamcomparison, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, "1"),
      '/teamcomparison/:season/': ({season}) => tc_route(endpoints.teamcomparison, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, "1"),
      // season and statnumber
      '/teamcomparison/:season/:stat': ({season, stat}) => tc_route(endpoints.teamcomparison, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, stat),
      '/teamcomparison/:season/:stat/': ({season, stat}) => tc_route(endpoints.teamcomparison, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, stat),

      // just the path
      '/playerstatistics': () => ps_route(endpoints.players, endpoints.playerstatistics, language, selectedSeason, selectedSeason, setSelectedSeason, selectedStat, changeStat, null, null),
      '/playerstatistics/:season': ({season}) => ps_route(endpoints.players, endpoints.playerstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, null, null),
      '/playerstatistics/:season/': ({season}) => ps_route(endpoints.players, endpoints.playerstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, null, null),
      // season and player
      '/playerstatistics/:season/:player': ({season, player}) => ps_route(endpoints.players, endpoints.playerstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, player, null),
      '/playerstatistics/:season/:player/': ({season, player}) => ps_route(endpoints.players, endpoints.playerstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, player, null),
      // season, player and stat
      '/playerstatistics/:season/:player/:stat': ({season, player, stat}) => ps_route(endpoints.players, endpoints.playerstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, player, stat),
      '/playerstatistics/:season/:player/:stat/': ({season, player, stat}) => ps_route(endpoints.players, endpoints.playerstatistics, language, selectedSeason, season, setSelectedSeason, selectedStat, changeStat, player, stat)
    })
}
