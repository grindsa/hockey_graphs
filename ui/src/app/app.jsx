import React, {useState, useEffect} from 'react';
import Cookies from 'universal-cookie';
import { LanguageSelector } from '../components/languageselector';
import { SeasonSelector } from '../components/seasonselector';
import { StatSelector } from '../components/statselector';
import { Routes } from '../components/routes'
import { navigate, useRoutes, useRedirect } from "hookrouter";
// import { Canvas } from '../components/canvas';
import { asyncGET, CookieSet, isEmpty } from '../components/sharedfunctions.js';
import { config } from '../components/constants.js';
import { creatstatList } from '../components/localization.js'

import '../css/mytheme.css';

const app_name = 'hockeygraphs@grinda'

// entry url for  backend
const rest_url = config.url.API_URL

export const App = () => {

  const [endpoints, setEndpoints] = useState([])
  const [seasonlist, setSeasonlist] = useState([])
  const [statList, setStatList] = useState([{id: 0, name: 'Spielstatistiken', route: '/matchstatistics'}, {id: 1, name: 'Teamvergleich', route: '/teamcomparison'}])
  const [language, setLanguage] = useState('DE')
  const [selectedSeason, setSelectedSeason] = useState(0)
  const [selectedStat, setSelectedStat] = useState(0)

  const changeSeason = (newSeason) => {
    // change season
    setSelectedSeason(newSeason)
    // update cookie
    CookieSet(app_name, {'selectedStat': selectedStat, 'endpoints': endpoints, 'language': language, 'selectedSeason': newSeason})

    // navigate to new season
    if (selectedStat == 1){
      navigate('/teamcomparison/' + newSeason);
    }else{
      navigate('/matchstatistics/' + newSeason)
    }
  }

  const changeStat = (newStat) => {
    // change stat
    setSelectedStat(newStat)
    // update cookie
    // CookieSet(app_name, {'selectedStat': newStat, 'endpoints': endpoints, 'language': language, 'selectedSeason': selectedSeason})
  }

  const toggleLanguage = () => {
    // change language
    setLanguage(language === 'DE' ? 'EN' : 'DE')
  }

  useEffect(() => {
    // similar to component did update fetchendpoint addresses
    const ep_get = async () => {
      const endpoints = await asyncGET(rest_url, 'endpoints')
      if (!isEmpty(endpoints)){
        setEndpoints(endpoints)
      }}
    ep_get()
    // parse cookie and read data
    const cookie = new Cookies();
    if (cookie.get(app_name)){
      // get and set language
      const languageValue = cookie.get(app_name).language
      setLanguage(languageValue)
      // get and set season
      const selectedseasonValue = cookie.get(app_name).selectedSeason
      setSelectedSeason(selectedseasonValue)
    }
  }, [])

  useEffect(() => {
    // monitor updates of language var and change statlist
    const newstatlist = creatstatList(language)
    setStatList(newstatlist)
    // update cookie
    CookieSet(app_name, {'selectedStat': selectedStat, 'endpoints': endpoints, 'language': language, 'selectedSeason': selectedSeason})
    },[language])

  useEffect(() => {
    // endpoint have changed - update season-list
    const sea_get = async () => {
      const seasonlist = await asyncGET(endpoints.seasons)
      if (!isEmpty(seasonlist)){
        setSeasonlist(seasonlist)
        // there is no season list defined in cookie take latest seasion
        if (selectedSeason === 0){
          var seasonid = seasonlist.results[seasonlist.count-1].id
          setSelectedSeason(seasonid)
        }
      }}
    sea_get()

    // update cookie
    CookieSet(app_name, {'selectedStat': selectedStat, 'endpoints': endpoints, 'language': language, 'selectedSeason': selectedSeason})
    },[endpoints])

  const routes = Routes(endpoints, language, selectedSeason, setSelectedSeason, selectedStat, changeStat)

  // define redirects
  // useRedirect('/', '/matchstatistics')
  useRedirect('/matchstatistics/', '/matchstatistics')
  useRedirect('/teamcomparison/', '/teamcomparison')

  const routeResult = useRoutes(routes);
  return (
    <div className="mainwidth">
      <div className="w3-bar pcolor">
        <SeasonSelector seasonValue={selectedSeason} seasonlist={ seasonlist.results } onchangeSeason={ changeSeason } />
        <StatSelector statlist={ statList } statValue={ selectedStat} onchangeStat={ changeStat }/>
        <a href="https://github.com/grindsa/hockey_graphs"><span className="w3-margin-right w3-round pcolor w3-right w3-margin-top">?</span></a>
        <LanguageSelector langValue={language } onClick={() => toggleLanguage()} />
      </div>
      <div>
      {routeResult}
      </div>
    </div>
  );
}
