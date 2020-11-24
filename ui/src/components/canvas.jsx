import React from 'react';
import { ChangeMatchday, MatchDayList } from '../components/matchday';

export class Canvas extends React.Component {

  render() {
    if(this.props.state.selectedStat === 0){
      return (
        <MatchDayList
          matchdays={this.props.state.endpoints.matchdays}
          matchstatistics={this.props.state.endpoints.matchstatistics}
          language={this.props.state.language}
          season={this.props.state.selectedSeason}
          />
      );
    }else{
      return (
        <h1> foo </h1>
      )
    }

  }
}
