import React, {useState, useEffect} from 'react';
import { MatchDayList } from '../components/matchday';
import { TeamComparison } from '../components/teamcomparison';

function tc_route(endpoint, language, selectedSeason, season, setSelectedSeason, stat){
  // update season and return TeamComparison route
  season = parseInt(season)
  if (season && selectedSeason && season && season !== selectedSeason) {
    setSelectedSeason(season)
  }
  return(
    <TeamComparison  teamcomparison={ endpoint } language={ language } season={ selectedSeason } stat={stat} />
  )
}

function mdl_route(ep_matchdays, ep_matchstatistics, language, selectedSeason, season, setSelectedSeason){
  // update season and return MatchDayList route
  season = parseInt(season)
  if (season && selectedSeason && season && season !== selectedSeason) {
    setSelectedSeason(season)
  }
  return(
    <MatchDayList matchdays={ep_matchdays} matchstatistics={ep_matchstatistics} language={language} season={season} />
  )

}

export const Routes = (endpoints, language, selectedSeason, selectedStat, setSelectedSeason) => {
    return ({
      '/': () => <MatchDayList matchdays={endpoints.matchdays} matchstatistics={endpoints.matchstatistics} language={language} season={selectedSeason} />,
      // just the path
      '/matchstatistics': () => <MatchDayList matchdays={endpoints.matchdays} matchstatistics={endpoints.matchstatistics} language={language} season={selectedSeason} />,
      // just the season
      '/matchstatistics/:season': ({season}) => mdl_route(endpoints.matchdays, endpoints.matchstatistics, language, selectedSeason, season, setSelectedSeason),

      // just the path
      '/teamcomparison': () => <TeamComparison  teamcomparison={ endpoints.teamcomparison } language={ language } season={ selectedSeason } stat={ selectedStat } />,
      // just the season
      '/teamcomparison/:season': ({season}) => tc_route(endpoints.teamcomparison, language, selectedSeason, season, setSelectedSeason, "1"),
      // season and statnumber
      '/teamcomparison/:season/:stat': ({season, stat}) => tc_route(endpoints.teamcomparison, language, selectedSeason, season, setSelectedSeason, stat)
    })
}
