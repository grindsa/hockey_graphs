import React from 'react';

import { ChangeMatchday, MatchDayList } from '../components/matchday'
import { GET, POST, asyncGET } from '../components/fetch.js';
import '../css/mytheme.css';


// entry url for  backend
const rest_url = 'http://127.0.0.1:8081/api/v1/';

export class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      endpoints: [],
    }
  }

  async componentDidMount(){
    // get rest endpoints
    const endpoints = await asyncGET(rest_url, 'endpoints')
    this.setState({endpoints: endpoints });
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
