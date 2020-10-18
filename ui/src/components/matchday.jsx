import React from 'react';
import { changeMatchDay }  from './matchdaystateservice';

export class MatchDayList extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      matchdaylist: [],
      date: '',
      currentKeyName: null,
      previousKeyName: null,
      nextKeyName: null,
    };
    this.handleMatchDayChange = this.handleMatchDayChange.bind(this);
  }

  async componentDidMount() {
    console.log('dismount')
    fetch('http://127.0.0.1:8081/api/v1/matchdays/')
    .then(res => res.json())
    .then(json => this.setState({ matchdaylist: json }))
    // .then(data => console.log('foo'));
  }

  filterMatchDay(Dictionary){
    // console.log(Dictionary)
    var MatchDay = []
    for(var keyName in Dictionary){
        if(Dictionary[keyName]['displayday']){
          MatchDay = Dictionary[keyName]['matches']
          this.state.date = Dictionary[keyName]['date']
          this.state.currentKeyName = keyName
          this.state.previousKeyName = Dictionary[keyName]['previous']
          this.state.nextKeyName = Dictionary[keyName]['next']
        }
    }
    return MatchDay
  }

  handleMatchDayChange(newDay){
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
        <p key={Match.match_id}>{Match.home_team} <img src={Match.home_team_logo} alt={Match.home_team} />{Match.result} <img src={Match.visitor_team_logo} alt={Match.visitor_team} />{Match.visitor_team}</p>
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
        <h3>{MatchDay}</h3>
      </React.Fragment>
    )
  }
}

export class ChangeMatchday extends React.Component {
  render(){
    return(
      <p>
        <a href='#' onClick={() => this.props.onChangeMatchDay(this.props.previous)}>p</a>
         {this.props.date}
        <a href='#' onClick={() => this.props.onChangeMatchDay(this.props.next)}>n</a>
      </p>
    )
  }
}
