import React from 'react';
import { MatchStatistics } from './matchstatistics';
import { ChangeMatchday } from './matchdaychange';
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
      selectedMatch: null,
    };
    this.handleMatchDayChange = this.handleMatchDayChange.bind(this);
    this.handleMatchSelect = this.handleMatchSelect.bind(this);
    this.resetMatchSelect = this.resetMatchSelect.bind(this);
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

  handleMatchSelect(selectedMatch){
    this.setState(currentState => {
      return {
        ... currentState,
        selectedMatch: selectedMatch
      }
    })
  }

  resetMatchSelect(){
    this.setState(currentState => {
      return {
        ... currentState,
        selectedMatch: null
      }
    })
  }

  render() {
    if(!this.state.selectedMatch){
      const MatchDay = this.filterMatchDay(this.state.matchdaylist).map((Match, index) =>{
        return(
          <tr key={Match.match_id} className="w3-hover-blue" onClick={() => this.handleMatchSelect(Match)}>
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
            language={this.props.language}
          />
          <table className="w3-table-all w3-hoverable"><tbody>{MatchDay}</tbody></table>
        </React.Fragment>
      )
    }else{
      return(
        <MatchStatistics match={this.state.selectedMatch} reset={this.resetMatchSelect} />
      )
    }
  }
}
