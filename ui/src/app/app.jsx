import React from 'react';

import { MatchDayList } from '../components/matchday'

// entry url for  backend
const rest_url = 'http://127.0.0.1:8081/api/v1/';

export class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      endpoints: [],
    }
  }

  componentDidMount(){
    fetch(rest_url)
    .then(res => res.json())
    .then(data => this.setState({ endpoints: data }));
  }

  render() {
    return (
      <React.Fragment>
        <h1> hello world! </h1>
        <MatchDayList url={this.state.endpoints.matchdays}/>
      </React.Fragment>
    );
  }
}
