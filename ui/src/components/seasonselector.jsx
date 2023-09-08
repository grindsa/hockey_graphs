import React from 'react';
import PropTypes from "prop-types";

export const SeasonSelector = (props) => {
  /* show select season */
  const getShortcut = (seasonValue, seasonlist) => {
    var seasonname = ''
    var color = 'pcolor'
    if (seasonValue != 0){
      for(var key in seasonlist) {
        if (seasonlist[key].id === seasonValue){
          seasonname = seasonlist[key].name
          // color pink if magenta sponsored events get selected
          if (seasonlist[key].name.includes('agenta')){
            color = 'w3-pink'
          }else if (seasonlist[key].name.includes('2024')) {
            color = 'pdelcolor'
          }
          break
        }
      }
    }
    const classNames = 'w3-tag w3-round w3-border ' + color
    return[seasonname, classNames]
  }

  const [seasonname, classNames] = getShortcut(props.seasonValue, props.seasonlist)
  return (
    <div className = "w3-dropdown-hover w3-left w3-margin">
      <div className = "pcolor">
        <span className={classNames}>{seasonname}</span>
      </div>
      <SeasonList seasonlist={ props.seasonlist } onchangeSeason={ props.onchangeSeason }/>
    </div>
  );
}

SeasonSelector.propTypes = {
    seasonValue: PropTypes.number.isRequired,
    seasonlist: PropTypes.array,
    onchangeSeason: PropTypes.func.isRequired,
};

const SeasonList = ({seasonlist, onchangeSeason}) => {
  /* build a list of seasons */
  let mlist
  if (seasonlist){
    mlist = seasonlist.map((season, index) =>{
      return(<div key={index} className = "w3-bar-item w3-button" onClick={() => onchangeSeason(season.id)}>{season.name}</div>)
    });
  }
  return(
    <div className = "w3-dropdown-content w3-bar-block w3-border pcolor">
      {mlist}
    </div>
  )
}

SeasonList.propTypes = {
    seasonlist: PropTypes.array,
    onchangeSeason: PropTypes.func.isRequired,
};
