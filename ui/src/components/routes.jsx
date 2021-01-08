import React, {useState, useEffect} from 'react';
import { MatchDayList } from '../components/matchday';
import { TeamComparison } from '../components/teamcomparison';

export const SiteRoutes = (endpoints, language, selectedSeason, selectedStat, setSelectedSeason) => {
    return ({
      '/matchstatistics': () => <MatchDayList />,
      '/teamcomparison': () => <TeamComparison  teamcomparison={ endpoints.teamcomparison } language={ language } season={ selectedSeason } stat={ selectedStat } />,
      '/teamcomparison/:season': ({season}) => {
        season = parseInt(season)
        if (season && selectedSeason && season && season !== selectedSeason) {
          setSelectedSeason(season)
        }
        return(
          <TeamComparison  teamcomparison={ endpoints.teamcomparison } language={ language } season={ selectedSeason } stat="1" />
        )
      },
      '/teamcomparison/:season/:stat': ({season, stat}) => {
        season = parseInt(season)
        if (season && selectedSeason && season && season !== selectedSeason) {
          setSelectedSeason(season)
        }
        return(
          <TeamComparison  teamcomparison={ endpoints.teamcomparison } language={ language } season={ selectedSeason } stat={stat} />
        )
      },
    })
}
