import React from 'react';
import { MatchDayList } from '../components/matchday';
import { TeamComparison } from '../components/teamcomparison';

export const Canvas = (props) => {
  if(props.selectedStat === 0){
    return (
      <MatchDayList
        matchdays={props.endpoints.matchdays}
        matchstatistics={props.endpoints.matchstatistics}
        language={props.language}
        season={props.selectedSeason}
        />
    );
  }else{
    return (
      <TeamComparison
        teamcomparison={props.endpoints.teamcomparison}
        language={props.language}
        season={props.selectedSeason}
        />
    )
  }
}
