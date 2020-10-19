import React from 'react';

import { ChangeMatchday, MatchDayList } from '../components/matchday'
import { LanguageSelector } from '../components/languageselector'
import { GET, POST, asyncGET } from '../components/fetch.js';
import '../css/mytheme.css';


// entry url for  backend
const rest_url = 'http://127.0.0.1:8081/api/v1/';

export class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      endpoints: [],
      language: 'EN',
    }
  }

  async componentDidMount(){
    // get rest endpoints
    const endpoints = await asyncGET(rest_url, 'endpoints')
    this.setState({endpoints: endpoints });
  }

  toggleLanguage(){
      let { language } = this.state;
      this.setState({ language: language === 'DE' ? 'EN' : 'DE' });
  }

  render() {
    return (
      <React.Fragment>
        <div className="w3-bar w3-padding pcolor">
          <i className="fa fa-bars fa-lg w3-xlarge  w3-bar-item" />
          <LanguageSelector langValue={ this.state.language } onClick={() => this.toggleLanguage()} />
        </div>
        <MatchDayList url={this.state.endpoints.matchdays}/>
      </React.Fragment>
    );
  }
}
