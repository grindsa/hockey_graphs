import React from 'react';

export class MatchDayList extends React.Component {

  constructor(props) {
    super(props);
    this.state = { MatchDayList: [], Date: '' };
  }

  async componentDidMount() {
    console.log('dismount')
    fetch('http://127.0.0.1:8081/api/v1/matchdays/')
    .then(res => res.json())
    .then(json => this.setState({ MatchDayList: json }))
    // .then(data => console.log('foo'));
  }

  filterMatchDay(Dictionary){
    // console.log(Dictionary)
    var MatchDay = []
    for(var keyName in Dictionary){
        if(Dictionary[keyName]['displayday']){
          MatchDay = Dictionary[keyName]['matches']
          this.state.date = Dictionary[keyName]['date']
        }
    }
    return MatchDay
  }

  render() {
    const MatchDay = this.filterMatchDay(this.state.MatchDayList).map((Match, index) =>{
      return(
        <p key={Match.match_id}>{Match.home_team} {Match.result} {Match.visitor_team}</p>
      )
    });

    return (
      <React.Fragment>
        <h2>{this.state.date}</h2>
        <h3>{MatchDay}</h3>
      </React.Fragment>
    )
  }
}
