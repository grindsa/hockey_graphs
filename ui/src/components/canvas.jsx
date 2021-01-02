import React from 'react';
import { MatchDayList } from '../components/matchday';
import { TeamComparison } from '../components/teamcomparison';

export const Canvas = (props) => {
  if(props.state.selectedStat === 0){
    return (
      <MatchDayList
        matchdays={props.state.endpoints.matchdays}
        matchstatistics={props.state.endpoints.matchstatistics}
        language={props.state.language}
        season={props.state.selectedSeason}
        />
    );
  }else{
    return (
      <TeamComparison
        teamcomparison={props.state.endpoints.teamcomparison}
        language={props.state.language}
        season={props.state.selectedSeason}
        />
    )
  }
}
