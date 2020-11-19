import React from 'react';

export class SeasonSelector extends React.Component {

  constructor(props) {
    super(props);
  }

  getShortcut(seasonValue, seasonlist){
    var seasonname = ''
    var color = 'pcolor'
    if (seasonValue != 0){
      for(var key in seasonlist) {
        if (seasonlist[key].id === seasonValue){
          seasonname = seasonlist[key].name
          // color pink if magenta sponsored events get selected
          if (seasonlist[key].name.includes('agenta')){
            color = 'w3-pink'
          }
          break
        }
      }
    }
    const classNames = 'w3-tag w3-round w3-border ' + color
    return[seasonname, classNames]
  }

  render() {
    const [seasonname, classNames] = this.getShortcut(this.props.seasonValue, this.props.seasonlist)
    return (
      <div className = "w3-dropdown-hover w3-left">
        <button className = "w3-button pcolor">
          <span className={classNames}>{seasonname}</span>
        </button>
        <SeasonList seasonlist={ this.props.seasonlist } onchangeSeason={ this.props.onchangeSeason }/>
      </div>
    );
  }
}

class SeasonList extends React.Component {

  constructor(props) {
    super(props);
  }

  render(){
    if (this.props.seasonlist){
      var mlist = this.props.seasonlist.map((season, index) =>{
        return(<div key={index} className = "w3-bar-item w3-button" onClick={() => this.props.onchangeSeason(season.id)}>{season.name}</div>)
      });
    }else{
      let mlist
    }
    return(
      <div className = "w3-dropdown-content w3-bar-block w3-border pcolor">
        {mlist}
      </div>
    )
  }
}
