import React, {useState, useEffect} from 'react';
import PropTypes from "prop-types";
import { overviewClassnames } from './matchstatisticservice.js';

export const MatchOverview = ({options}) => {
  // matchoverview shoing shots, gols, toi and penalties
  const stats = options
  return(
    <div className="w3-border prematch_container w3-display-container">
      <img className="w3-opacity-max" style={{width:'100%'}} src={stats.background_image}></img>
      <div className="content">
        <div>
          <div className="w3-container w3-center w3-jumbo uc strong">{stats.title}</div>
            <div className="w3-center w3-row">
              <div className="w3-col w3-row" style={{width:'40%'}}>
                  <div className="w3-col w3-margin-left" style={{width:'50%'}}>
                    <div className="strong w3-tiny alignleft">{stats.shotEfficiency}: {stats.home_team.shotEfficiency_pctg}</div>
                    <div className="w3-container w3-light-grey w3-tiny nopadding"><div style={{width:stats.home_team.shotEfficiency_pctg, backgroundColor:stats.home_team.team_color, color: '#ffffff'}}>&nbsp;</div></div>
                    <div className="strong w3-tiny w3-margin-top alignleft">{stats.puckpossession}: {stats.home_team.puckpossession_pctg}</div>
                    <div className="w3-container w3-light-grey w3-tiny nopadding"><div style={{width:stats.home_team.puckpossession_pctg, backgroundColor:stats.home_team.team_color, color: '#ffffff'}}>&nbsp;</div></div>
                  </div>
                  <div className="w3-col" style={{width:'40%'}}>
                    <img className="w3-right" src={stats.home_team.logo} alt={stats.home_team.shortcut} height="80px"></img>
                  </div>
              </div>
              <div className="w3-col w3-margin-top horizontal-middle" style={{width:'20%'}}><i className="w3-xxxlarge fa fa-bolt"></i></div >
              <div className="w3-col w3-row" style={{width:'40%'}}>
                <div className="w3-col w3-margin-left" style={{width:'40%'}}>
                  <img className="w3-left" src={stats.visitor_team.logo} alt={stats.visitor_team.shortcut} height="80px"></img>
                </div>
                <div className="w3-col" style={{width:'50%'}}>
                  <div className="strong w3-tiny alignright">{stats.shotEfficiency}: {stats.visitor_team.shotEfficiency_pctg}</div>
                  <div className="w3-container w3-light-grey w3-tiny nopadding"><div className="w3-right" style={{width: stats.visitor_team.shotEfficiency_pctg, backgroundColor:stats.visitor_team.team_color, color: '#ffffff'}}>&nbsp;</div></div>
                  <div className="strong w3-tiny w3-margin-top alignright">{stats.puckpossession}: {stats.visitor_team.puckpossession_pctg}</div>
                  <div className="w3-container w3-light-grey w3-tiny nopadding"><div className="w3-right" style={{width: stats.visitor_team.puckpossession_pctg, backgroundColor:stats.visitor_team.team_color, color: '#ffffff'}}>&nbsp;</div></div>
                </div>
              </div >
            </div>
        </div>
        <div>
          <div className="w3-section w3-row-padding w3-center">
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.goals}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team.team_color}}>{stats.home_team.goals}</div>
                <div className="w3-half" style={{color:stats.visitor_team.team_color}}>{stats.visitor_team.goals}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.powerplay}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team.team_color}}>{stats.home_team.powerplay}</div>
                <div className="w3-half" style={{color:stats.visitor_team.team_color}}>{stats.visitor_team.powerplay}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.penaltyMinutes}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team.team_color}}>{stats.home_team.penaltyMinutes}</div>
                <div className="w3-half" style={{color:stats.visitor_team.team_color}}>{stats.visitor_team.penaltyMinutes}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.faceOffsWon}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team.team_color}}>{stats.home_team.faceOffsWon}</div>
                <div className="w3-half" style={{color:stats.visitor_team.team_color}}>{stats.visitor_team.faceOffsWon}</div>
              </div>
            </div>
          </div>
          <div className="w3-section w3-row-padding w3-center">
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.shots}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team.team_color}}>{stats.home_team.shots}</div>
                <div className="w3-half" style={{color:stats.visitor_team.team_color}}>{stats.visitor_team.shots}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.shotsOnGoal}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team.team_color}}>{stats.home_team.shotsOnGoal}</div>
                <div className="w3-half" style={{color:stats.visitor_team.team_color}}>{stats.visitor_team.shotsOnGoal}</div>
              </div>
            </div>
            <div className="w3-quarter">
            <div className="w3-container pcolor w3-padding-small">{stats.saves}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team.team_color}}>{stats.home_team.saves}</div>
                <div className="w3-half" style={{color:stats.visitor_team.team_color}}>{stats.visitor_team.saves}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.shotsBlocked}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team.team_color}}>{stats.home_team.shotsBlocked}</div>
                <div className="w3-half" style={{color:stats.visitor_team.team_color}}>{stats.visitor_team.shotsBlocked}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className="w3-display-bottomright cpr">@2022 GrindSa <a href="https://hockeygraphs.dynamop.de">(https://hockeygraphs.dynamop.de)</a></div>
    </div>
  )
}

MatchOverview.propTypes = {
    options: PropTypes.object,
};

const TableRow = (props) => {
  /* single row in matchstats we need to assing color classes based on values */
  var [leftClassNames, rightClassNames] = overviewClassnames(props.leftvalue, props.rightvalue)
  return (
    <React.Fragment>
      <tr><td colSpan="2" className="w3-small"><b>{props.statname}</b></td></tr>
      <tr>
          <td style={{width:'50%'}}><div className="w3-container w3-light-grey w3-tiny nopadding"><div className={leftClassNames} style={{width:props.leftwidth}}>{props.leftvalue}</div></div></td>
          <td style={{width:'50%'}}><div className="w3-container w3-light-grey w3-tiny nopadding"><div className={rightClassNames} style={{width:props.rightwidth}}>{props.rightvalue}</div></div></td>
      </tr>
    </React.Fragment>
  )
}

TableRow.propTypes = {
    leftvalue: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    leftwidth: PropTypes.string,
    rightvalue: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
    rightwidth: PropTypes.string,
    statname: PropTypes.string,
};
