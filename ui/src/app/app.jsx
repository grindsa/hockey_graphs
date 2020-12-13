import React from 'react';

import Cookies from 'universal-cookie';
import { LanguageSelector } from '../components/languageselector';
import { SeasonSelector } from '../components/seasonselector';
import { StatSelector } from '../components/statselector';
import { Canvas } from '../components/canvas';
import { asyncGET, CookieSet } from '../components/sharedfunctions.js';
import { config } from '../components/constants.js';
import { creatstatList } from '../components/localization.js'
import '../css/mytheme.css';

const app_name = 'hockeygraphs@grinda'

// entry url for  backend
const rest_url = config.url.API_URL

export class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      endpoints: [],
      seasonlist: [],
      language: 'DE',
      selectedSeason: 0,
      StatList: [{id: 0, name: 'Spielstatistiken'}, {id: 1, name: 'Teamvergleich'}],
      selectedStat: 0
    }

    this.changeSeason = this.changeSeason.bind(this);
    this.changeStat = this.changeStat.bind(this);
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
    // create list of stat based on language preferences
    const statlist = creatstatList(this.state.language)
    this.setState({StatList: statlist });
  }

  async changeSeason(newSeason){
    // change season
    await this.setState({selectedSeason: newSeason})
    // update cookie
    CookieSet(app_name, this.state)
  }

  async changeStat(newStat){
    // change stat
    await this.setState({selectedStat: newStat})
    // update cookie
    // const cookies = new Cookies();
    // cookies.set(app_name, {language: this.state.language, selectedSeason: this.state.selectedSeason, foo: 'WannaSeeUrFaceOnceUreadThis'}, { path: '/', maxAge: 2419200 });
  }

  async toggleLanguage(){
    let { language } = this.state;
    // change language
    await this.setState({ language: language === 'DE' ? 'EN' : 'DE' });
    // update cookie
    CookieSet(app_name, this.state)
    // create list of stat based on language preferences
    const statlist = creatstatList(this.state.language)
    this.setState({StatList: statlist });
  }

  render() {
    // <i className="far fa-square fa-lg w3-xlarge  w3-bar-item" />
    return (
      <div className="mainwidth">
        <div className="w3-bar pcolor">
          <SeasonSelector seasonValue={this.state.selectedSeason} seasonlist={ this.state.seasonlist.results } onchangeSeason={ this.changeSeason } />
          <StatSelector statlist={this.state.StatList} statValue={this.state.selectedStat} onchangeStat={ this.changeStat }/>
          <a href="https://github.com/grindsa/hockey_graphs"><span className="w3-margin-right w3-round pcolor w3-right w3-margin-top">?</span></a>
          <LanguageSelector langValue={ this.state.language } onClick={() => this.toggleLanguage()} />
        </div>
        <Canvas state={this.state} />
      </div>
    );
  }
}
