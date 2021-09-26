import React from 'react';
import PropTypes from "prop-types";
import { A } from "hookrouter";

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

StatSelector.propTypes = {
    statValue: PropTypes.number.isRequired,
    statlist: PropTypes.array.isRequired,
    onchangeStat: PropTypes.func.isRequired,
};

const StatList = ({statlist, onchangeStat}) => {
  // generate list of stats
  let mlist
  if (statlist){
    mlist = statlist.map((stat, index) =>{
      // hack to deactivate playerstats before its ready
      if(stat.id < 2){
        return(<div key={index} className = "w3-bar-item w3-button" onClick={() => onchangeStat(stat.id)}><A href={stat.route} className="nopadding">{stat.name}</A></div>)
      }
    });
  }
  return(
    <div className = "w3-dropdown-content w3-bar-block w3-border pcolor">
      {mlist}
    </div>
  )
}

StatList.propTypes = {
    statlist: PropTypes.array.isRequired,
    onchangeStat: PropTypes.func.isRequired,
};
