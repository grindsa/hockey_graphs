import React from 'react';

export const StatSelector = (props) => {
  // show selected stat-option
  return (
    <div className = "w3-dropdown-hover w3-left w3-margin-top">
      <div className = "pcolor">
        <span className="w3-tag w3-round w3-border pcolor">{ props.statlist[props.statValue].name }</span>
        <StatList statlist={ props.statlist } onchangeStat={ props.onchangeStat }/>
      </div>
    </div>
  );
}

const StatList = ({statlist, onchangeStat}) => {
  // generate list of stats
  if (statlist){
    var mlist = statlist.map((stat, index) =>{
      return(<div key={index} className = "w3-bar-item w3-button" onClick={() => onchangeStat(stat.id)}>{stat.name}</div>)
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
