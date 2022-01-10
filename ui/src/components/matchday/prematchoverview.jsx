import React, {useState, useEffect} from 'react';
import PropTypes from "prop-types";
import { isMobileOnly } from 'react-device-detect';
import { overviewClassnames } from './matchstatisticservice.js';

export const PreMatchOverview = ({options}) => {
  // matchoverview shoing shots, gols, toi and penalties
  const stats = options

  if (isMobileOnly){
    var headline_classes = "w3-xlarge"
    var img_classes = "hidden"
    var footer_classes = "hidden"
  } else {
    var headline_classes = "w3-jumbo"
    var img_classes = "w3-opacity-max"
    var footer_classes = "w3-display-bottomright "
  }

  console.log(stats.h2h_results)
  const MatchTable = stats.h2h_results.map((Match) =>{
    return(
      <tr key={Match.match_id} className="strong">
        <td>{Match.date}</td>
        <td><img src={Match.home_team_logo} alt={Match.home_team_shortcut} width="20px"></img></td>
        <td>{Match.result}</td>
        <td><img src={Match.visitor_team_logo} alt={Match.visitor_team_shortcut} width="20px"></img></td>
      </tr>
    )
  });

  return(
    <div className="w3-border prematch_container w3-display-container">
      <img className={img_classes} style={{width:'100%'}} src={stats.background_image}></img>
      <div className="content">
        <div>
          <div className={"w3-container w3-center uc strong " + headline_classes}>{stats.title}</div>
            <div className="w3-center w3-row">
              <div className="w3-col" style={{width:'20%'}}>
                <img className="w3-right" src={stats.home_team_logo} alt={stats.home_team_shortcut} height="80px"></img>
              </div>
              <div className="w3-col w3-margin-top horizontal-middle" style={{width:'20%'}}><i className="w3-xxxlarge fa fa-bolt"></i></div >
              <div className="w3-col" style={{width:'23%'}}>
                <img className="w3-left" src={stats.visitor_team_logo} alt={stats.visitor_team_shortcut} height="80px"></img>
              </div >
              <div className="w3-col" style={{width:'35%'}}>
                <div className="w3-left">
                  <table className="w3-table w3-small w3-light-grey w3-border w3-border-dark-grey">
                    <tbody>
                      {MatchTable}
                    </tbody>
                  </table>
                </div>
              </div >
            </div>
            <div className="w3-row w3-margin-top">
              <div className="w3-col" style={{width:'30%'}}>
                <div className="w3-center w3-large strong">{stats.home_bilance} ({stats.home_last10})</div>
              </div>
              <div className="w3-col" style={{width:'32%'}}>
                <div className="w3-center w3-large strong">{stats.visitor_bilance} ({stats.visitor_last10})</div>
              </div >
            </div>
        </div>

        <div>
          <div className="w3-section w3-row-padding w3-center">
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">Power Play %</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team_color}}>{stats.home_pp_pctg}</div>
                <div className="w3-half" style={{color:stats.visitor_team_color}}>{stats.visitor_pp_pctg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">Penalty Kill %</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team_color}}>{stats.home_pk_pctg}</div>
                <div className="w3-half" style={{color:stats.visitor_team_color}}>{stats.visitor_pk_pctg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">PDO</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team_color}}>{stats.home_pdo}</div>
                <div className="w3-half" style={{color:stats.visitor_team_color}}>{stats.visitor_pdo}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.txt_fac} %</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team_color}}>{stats.home_fac_pctg}</div>
                <div className="w3-half" style={{color:stats.visitor_team_color}}>{stats.visitor_fac_pctg}</div>
              </div>
            </div>
          </div>

          <div className="w3-section w3-row-padding w3-center">
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.txt_gfpg}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team_color}}>{stats.home_goals_for_pg}</div>
                <div className="w3-half" style={{color:stats.visitor_team_color}}>{stats.visitor_goals_for_pg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.txt_gapg}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team_color}}>{stats.home_goals_against_pg}</div>
                <div className="w3-half" style={{color:stats.visitor_team_color}}>{stats.visitor_goals_against_pg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.txt_sfpg}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team_color}}>{stats.home_shots_ongoal_for_pg}</div>
                <div className="w3-half" style={{color:stats.visitor_team_color}}>{stats.visitor_shots_ongoal_for_pg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">{stats.txt_sapg}</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half" style={{color:stats.home_team_color}}>{stats.home_shots_ongoal_against_pg}</div>
                <div className="w3-half" style={{color:stats.visitor_team_color}}>{stats.visitor_shots_ongoal_against_pg}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div className={"cpr " + footer_classes}>@2022 GrindSa <a href="https://hockeygraphs.dynamop.de">(https://hockeygraphs.dynamop.de)</a></div>
    </div>
  )
}
