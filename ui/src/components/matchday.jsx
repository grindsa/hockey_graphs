import React, {useState, useEffect} from 'react';
import { MatchStatistics } from './matchday/matchstatistics';
import { ChangeMatchday } from './matchday/matchdaychange';
import { changeMatchDay, getMatch }  from './matchday/matchdaystateservice';
import { asyncGET, isEmpty } from './sharedfunctions.js';
import { navigate } from "hookrouter";

export const MatchDayList = (props) => {

  // class which creates and displays list of matches for cert day
  const [matchdaydic, setMatchdaydic] = useState({})
  const [selectedMatch, setSelectedMatch] = useState(null)

  // initialize some variables we need
  var mdate = ''
  var [currentKeyName, setCurrentKeyName] = useState(null)
  var previousKeyName = null
  var nextKeyName = null

  const filterMatchDay = (Dictionary) => {
    /* filter certain matchday out of matchdaydic */
    var MatchDay = []
    for(var keyName in Dictionary){
        /* skip all matchdays with displayday false */
        if(Dictionary[keyName]['displayday']){
          /* list of days will be stored in a local variable as it is not needed in states */
          MatchDay = Dictionary[keyName]['matches']
          /* we need these variables in other functions thus lets put them into state */
          mdate = Dictionary[keyName]['date']
          currentKeyName = keyName
          previousKeyName = Dictionary[keyName]['previous']
          nextKeyName = Dictionary[keyName]['next']
          break;
        }
    }
    return  MatchDay
  }

  const handleMatchDayChange = (newDay) => {
    /* this is a handler for a matchday change we call a function and update the state */
    setMatchdaydic(changeMatchDay(matchdaydic, currentKeyName, newDay))
    setCurrentKeyName(newDay)
  }

  const handleMatchSelect = (selectedMatch, stat=null, redirect=true) => {
    /* handler triggerd by clickcing on a single match */
    setSelectedMatch(selectedMatch)
    if (stat && redirect){
      navigate('/matchstatistics/' + props.season + '/' + selectedMatch['match_id'] + '/' + stat);
    }else if (redirect){
      navigate('/matchstatistics/' + props.season + '/' + selectedMatch['match_id'] )
    }
  }

  const handleDayClick = (day) => {
    /* handler triggered when picking a date from calendar */
    var newDate = day.toISOString().substring(0, 10)
    handleMatchDayChange(newDate)
  }

  const resetMatchSelect = () => {
    /* handler triggered by back button in matchstatistics */
    setSelectedMatch(null)
    if(props.matchid){
      // we need to navigate if we get a reset and a match
      navigate('/matchstatistics/' + props.season )
    }
  }

  useEffect(() => {
    if (props.matchdays &&  props.season) {
      const md_get = async () => {
        const md_dic = await asyncGET(props.matchdays + '?season=' + props.season)
        if (!isEmpty(md_dic)){
          setMatchdaydic(md_dic);
        }
      }
      md_get()
    }

  }, [props.matchdays,  props.season])

  if(props.matchid && !isEmpty(matchdaydic)) {
    const [matchday, selMatch] = getMatch(matchdaydic, props.matchid)
    if (selMatch != selectedMatch){
      handleMatchSelect(selMatch, props.stat, false)
    }
    if (matchday != currentKeyName){
      handleMatchDayChange(matchday)
    }
  }

  if(!selectedMatch){
    const MatchDay = filterMatchDay(matchdaydic).map((Match) =>{
      return(
        <tr key={Match.match_id} className="w3-hover-blue" onClick={() => handleMatchSelect(Match)}>
          <td className="w3-right-align middle" style={{width:'35%'}}>{Match.home_team_name}</td>
          <td className="w3-right-align middle" style={{width:'10%'}}><img src={Match.home_team_logo} alt={Match.home_team_shortcut} width="40px"/></td>
          <td className={"w3-center middle result_finish_" + Match.finish} style={{width:'10%'}}>{Match.result} </td>
          <td className="w3-left-align middle" style={{width:'10%'}}><img src={Match.visitor_team_logo} alt={Match.visitor_team_shortcut} width="40px"/></td>
          <td className="w3-left-align middle" style={{width:'35%'}}>{Match.visitor_team_name}</td>
        </tr>
      )
    });
    return (
      <React.Fragment>
        <ChangeMatchday
          date={mdate}
          next={nextKeyName}
          previous={previousKeyName}
          onChangeMatchDay={handleMatchDayChange}
          language={props.language}
          matchdaylist = {Object.keys(matchdaydic)}
          current={currentKeyName}
          handleDayClick = {handleDayClick}
        />
        <table className="w3-table-all w3-hoverable"><tbody>{MatchDay}</tbody></table>
      </React.Fragment>
    )
  }else{
    return(
      <MatchStatistics season={props.season} match={selectedMatch} matchstatistics={props.matchstatistics} reset={resetMatchSelect} language={props.language} stat={props.stat}/>
    )
  }
}
