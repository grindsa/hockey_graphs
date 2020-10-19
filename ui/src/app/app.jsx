import React from 'react';

import { ChangeMatchday, MatchDayList } from '../components/matchday'
import { GET, POST } from '../components/fetch.js';

// entry url for  backend
const rest_url = 'http://127.0.0.1:8081/api/v1/';

export class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      endpoints: [],
      matchdays: {},
    }
  }

  async componentDidMount(){
    // get rest endpoints
    const endpoints = await this.getData(rest_url, 'endpoints')
    // get matchdays
    // const matchdays = await this.getData(this.state.endpoints.matchdays, 'matchdays')
  }

  async getData(apiEndpoint, parameter) {
    if(apiEndpoint){
      const { data: Items } = await GET(apiEndpoint);
      if (Items) {
        this.setState({[parameter]: Items });
      }else{
        // error
      }
    }
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
