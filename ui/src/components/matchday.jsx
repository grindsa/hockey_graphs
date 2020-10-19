import React from 'react';
import { changeMatchDay }  from './matchdaystateservice';
import { asyncGET } from './fetch.js';


export class MatchDayList extends React.Component {
  /* class which creates and displays list of matches for cert day */
  constructor(props) {
    super(props);
    this.state = {
      matchdaylist: {},
      date: '',
      currentKeyName: null,
      previousKeyName: null,
      nextKeyName: null,
    };
    this.handleMatchDayChange = this.handleMatchDayChange.bind(this);
  }

  async componentDidUpdate(prevProps) {
    /* we get the url to fectch as props and monitor it here */
    if (this.props.url !== prevProps.url) {
        // get matchdays
        const matchdaylist = await asyncGET(this.props.url)
        this.setState({matchdaylist: matchdaylist });
    }
  }

  filterMatchDay(Dictionary){
    /* filter certain matchday out of matchdaylist */
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
        matchdaylist: changeMatchDay(currentState.matchdaylist, currentState.currentKeyName, newDay)
      }
    })
  }

  render() {
    const MatchDay = this.filterMatchDay(this.state.matchdaylist).map((Match, index) =>{
      return(
        <tr key={Match.match_id}>
          <td className="w3-right-align middle">{Match.home_team_name}</td>
          <td className="w3-right-align middle"><img src={Match.home_team_logo} alt={Match.home_team_shortcut} width="40px"/></td>
          <td className="w3-center result middle">{Match.result} </td>
          <td className="w3-left-align middle"><img src={Match.visitor_team_logo} alt={Match.visitor_team_shortcut} width="40px"/></td>
          <td className="w3-left-align middle">{Match.visitor_team_name}</td>
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
        />
        <table className="w3-table-all">
        <tbody>
          {MatchDay}
        </tbody>
        </table>
      </React.Fragment>
    )
  }
}

export class ChangeMatchday extends React.Component {
  /* this class displays a header allowing matchday changes */
  render(){
    return(
      <div className="w3-container w3-padding-small pcolor w3-section w3-center">
        <h1>
          <a href='#' onClick={() => this.props.onChangeMatchDay(this.props.previous)}><i className="w3-margin-right fa fa-arrow-left" /></a>
           {this.props.date}
          <a href='#' onClick={() => this.props.onChangeMatchDay(this.props.next)}><i className="w3-margin-left fa fa-arrow-right" /></a>
        </h1>
      </div>
    )
  }
}
