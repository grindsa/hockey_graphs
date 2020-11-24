import React from 'react';
import { MatchStatistics } from './matchday/matchstatistics';
import { ChangeMatchday } from './matchday/matchdaychange';
import { changeMatchDay, checkMatchdayUpdate }  from './matchday/matchdaystateservice';
import { asyncGET } from './sharedfunctions.js';


export class MatchDayList extends React.Component {
  /* class which creates and displays list of matches for cert day */

  constructor(props) {
    super(props);
    this.state = {
      matchdaydic: {},
      date: '',
      currentKeyName: null,
      previousKeyName: null,
      nextKeyName: null,
      selectedMatch: null,
    };
    this.handleMatchDayChange = this.handleMatchDayChange.bind(this);
    this.handleMatchSelect = this.handleMatchSelect.bind(this);
    this.resetMatchSelect = this.resetMatchSelect.bind(this);
    this.handleDayClick = this.handleDayClick.bind(this);
  }

  async componentDidMount(){
    if (this.props.matchdays && this.props.season) {
      // get matchdays
      const matchdaydic = await asyncGET(this.props.matchdays + '?season=' + this.props.season)
      this.setState({matchdaydic: matchdaydic});
    }
  }

  async componentDidUpdate(prevProps) {
    /* we get the url to fectch as props and monitor it here */
    const matchdaysupdate = checkMatchdayUpdate(this.props.matchdays, prevProps.matchdays, this.props.season, prevProps.season)
    if (matchdaysupdate){
        // get matchdays
        const matchdaydic = await asyncGET(this.props.matchdays + '?season=' + this.props.season)
        this.setState({matchdaydic: matchdaydic});
    }
  }

  filterMatchDay(Dictionary){
    /* filter certain matchday out of matchdaydic */
    var MatchDay = []
    for(var keyName in Dictionary){
        /* skip all matchdays with displayday false */
        if(Dictionary[keyName]['displayday']){
          /* list of days will be stored in a local variable as it is not needed in states */
          MatchDay = Dictionary[keyName]['matches']
          /* we need these variables in other functions thus lets put them into state */
          this.state.date = Dictionary[keyName]['date']
          this.state.currentKeyName = keyName
          this.state.previousKeyName = Dictionary[keyName]['previous']
          this.state.nextKeyName = Dictionary[keyName]['next']
        }
    }
    return MatchDay
  }

  handleMatchDayChange(newDay){
    /* this is a handler for a matchday change we call a function and update the state */
    this.setState(currentState => {
      return {
        ... currentState,
        matchdaydic: changeMatchDay(currentState.matchdaydic, currentState.currentKeyName, newDay),
        currentKeyName: newDay
      }
    })
  }

  handleMatchSelect(selectedMatch){
    /* handler triggerd by clickcing on a single match */
    this.setState(currentState => {
      return {
        ... currentState,
        selectedMatch: selectedMatch
      }
    })
  }

  async handleDayClick(day) {
    /* handler triggered when picking a date from calendar */
    var newDate = day.toISOString().substring(0, 10)
    await this.handleMatchDayChange(newDate)
  }

  resetMatchSelect(){
    /* handler triggered by back button in matchstatistics */
    this.setState(currentState => {
      return {
        ... currentState,
        selectedMatch: null
      }
    })
  }

  render() {
    if(!this.state.selectedMatch){
      const MatchDay = this.filterMatchDay(this.state.matchdaydic).map((Match, index) =>{
        return(
          <tr key={Match.match_id} className="w3-hover-blue" onClick={() => this.handleMatchSelect(Match)}>
            <td className="w3-right-align middle" style={{width:'35%'}}>{Match.home_team_name}</td>
            <td className="w3-right-align middle" style={{width:'10%'}}><img src={Match.home_team_logo} alt={Match.home_team_shortcut} width="40px"/></td>
            <td className="w3-center result middle" style={{width:'10%'}}>{Match.result} </td>
            <td className="w3-left-align middle" style={{width:'10%'}}><img src={Match.visitor_team_logo} alt={Match.visitor_team_shortcut} width="40px"/></td>
            <td className="w3-left-align middle" style={{width:'35%'}}>{Match.visitor_team_name}</td>
          </tr>
        )
      });
      return (
        <React.Fragment>
          <ChangeMatchday
            date={this.state.date}
            next={this.state.nextKeyName}
            previous={this.state.previousKeyName}
            onChangeMatchDay={this.handleMatchDayChange}
            language={this.props.language}
            matchdaylist = {Object.keys(this.state.matchdaydic)}
            current={this.state.currentKeyName}
            handleDayClick = {this.handleDayClick}
          />
          <table className="w3-table-all w3-hoverable"><tbody>{MatchDay}</tbody></table>
        </React.Fragment>
      )
    }else{
      return(
        <MatchStatistics match={this.state.selectedMatch} matchstatistics={this.props.matchstatistics} reset={this.resetMatchSelect} language={this.props.language}/>
      )
    }
  }
}
