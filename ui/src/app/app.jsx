import React from 'react';

import { MatchDayList } from '../components/matchday'

export class App extends React.Component {
  render() {
    return (
      <React.Fragment>
        <h1> hello world! </h1>
        <MatchDayList />
      </React.Fragment>        
    );
  }
}
