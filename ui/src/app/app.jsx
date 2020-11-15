import React from 'react';

import Cookies from 'universal-cookie';
import { ChangeMatchday, MatchDayList } from '../components/matchday';
import { LanguageSelector } from '../components/languageselector';
import { SeasonSelector } from '../components/seasonselector';
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
      seasonlist: [],
      language: 'DE',
      selectedSeason: 0,
    }

    this.changeSeason = this.changeSeason.bind(this);
  }

  async componentDidMount(){
    // get rest endpoints
    const endpoints = await asyncGET(rest_url, 'endpoints')
    this.setState({endpoints: endpoints });
    // get and set seasonlist
    const seasonlist = await asyncGET(endpoints.seasons)
    await this.setState({seasonlist: seasonlist});
    // seasonid
    if (this.state.selectedSeason === 0){
      var seasonid = this.state.seasonlist.results[this.state.seasonlist.count-1].id
      await this.setState({selectedSeason: seasonid});
    }
    // parse cookie
    const cookies = new Cookies();
    const langValue = cookies.get(app_name).language
    var selectedSeason = cookies.get(app_name).selectedSeason
    if(selectedSeason){
      await this.setState({selectedSeason: selectedSeason});
    }
    await this.setState({language: langValue });
  }

  async changeSeason(newSeason){
    // change season
    await this.setState({selectedSeason: newSeason})
    // update cookie
    const cookies = new Cookies();
    cookies.set(app_name, {language: this.state.language, selectedSeason: this.state.selectedSeason, foo: 'WannaSeeUrFaceOnceUreadThis'}, { path: '/', maxAge: 2419200 });
  }

  async toggleLanguage(){
    let { language } = this.state;
    // change language
    await this.setState({ language: language === 'DE' ? 'EN' : 'DE' });
    // update cookie
    const cookies = new Cookies();
    cookies.set(app_name, {language: this.state.language, selectedSeason: this.state.selectedSeason, foo: 'WannaSeeUrFaceOnceUreadThis'}, { path: '/', maxAge: 2419200 });
  }

  render() {
    return (
      <div className="mainwidth">
        <div className="w3-bar w3-padding pcolor">
          <i className="fa fa-bars fa-lg w3-xlarge  w3-bar-item" />
          <SeasonSelector seasonValue={this.state.selectedSeason} seasonlist={ this.state.seasonlist.results } onchangeSeason={ this.changeSeason } />
          <LanguageSelector langValue={ this.state.language } onClick={() => this.toggleLanguage()} />
        </div>
        <MatchDayList
          matchdays={this.state.endpoints.matchdays}
          matchstatistics={this.state.endpoints.matchstatistics}
          language={this.state.language}
          season={this.state.selectedSeason}
          />
      </div>
    );
  }
}
