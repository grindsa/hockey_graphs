import React from 'react';
import { MatchDayList } from '../components/matchday';
import { TeamComparison } from '../components/teamcomparison';
import { PlayerStatistic } from '../component/playerstatistic'

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
  }else if(props.selectedStat === 1){
    return (
      <TeamComparison
        teamcomparison={props.endpoints.teamcomparison}
        language={props.language}
        season={props.selectedSeason}
        />
    );
  }else{
    return (
      <PlayerStatistic
        playerlist={props.endpoints.players}
        language={props.language}
        season={props.selectedSeason}
        />
    )
  }
}
