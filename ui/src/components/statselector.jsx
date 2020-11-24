import React from 'react';

export class StatSelector extends React.Component {

  render() {
    return (
      <div className = "w3-dropdown-hover w3-left w3-margin-top">
        <div className = "pcolor">
          <span className="w3-tag w3-round w3-border pcolor">{this.props.statlist[this.props.statValue].name}</span>
          <StatList statlist={ this.props.statlist } onchangeStat={ this.props.onchangeStat }/>
        </div>
      </div>
    );
  }
}

class StatList extends React.Component {

  render(){
    if (this.props.statlist){
      var mlist = this.props.statlist.map((stat, index) =>{
        return(<div key={index} className = "w3-bar-item w3-button" onClick={() => this.props.onchangeStat(stat.id)}>{stat.name}</div>)
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
