import React from 'react';

import Cookies from 'universal-cookie';
import { ChangeMatchday, MatchDayList } from '../components/matchday'
import { LanguageSelector } from '../components/languageselector'
import { GET, POST } from '../components/fetch.js';
import { asyncGET } from '../components/sharedfunctions.js';
import '../css/mytheme.css';

const app_name = 'hockeygraphs@grinda'


// entry url for  backend
const rest_url = 'http://127.0.0.1:8081/api/v1/';

export class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      endpoints: [],
      language: 'DE',
    }
  }

  async componentDidMount(){
    // get rest endpoints
    const endpoints = await asyncGET(rest_url, 'endpoints')
    this.setState({endpoints: endpoints });
    const cookies = new Cookies();
    const langValue = cookies.get(app_name).language
    await this.setState({language: langValue });
  }

  async toggleLanguage(){
    let { language } = this.state;
    await this.setState({ language: language === 'DE' ? 'EN' : 'DE' });
    const cookies = new Cookies();
    cookies.set(app_name, {language: this.state.language, foo: 'WannaSeeUrFaceOnceUreadThis'}, { path: '/', maxAge: 2419200 });
  }

  render() {
    return (
      <React.Fragment>
        <div className="w3-bar w3-padding pcolor">
          <i className="fa fa-bars fa-lg w3-xlarge  w3-bar-item" />
          <LanguageSelector langValue={ this.state.language } onClick={() => this.toggleLanguage()} />
        </div>
        <MatchDayList matchdays={this.state.endpoints.matchdays} matchstatistics={this.state.endpoints.matchstatistics} language={this.state.language}/>
      </React.Fragment>
    );
  }
}
