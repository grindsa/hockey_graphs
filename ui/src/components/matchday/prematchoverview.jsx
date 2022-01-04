import React, {useState, useEffect} from 'react';
import PropTypes from "prop-types";
import { overviewClassnames } from './matchstatisticservice.js';

export const PreMatchOverview = ({options}) => {
  // matchoverview shoing shots, gols, toi and penalties
  const stats = options
  console.log(stats)
  return(
    <div className="w3-border prematch_container">
      <img className="w3-opacity-max" style={{width:'100%'}} src={stats.background_image}></img>
      <div className="content">
        <div>
          <div className="w3-container w3-center w3-jumbo uc strong">{stats.title}</div>
            <div className="w3-center">
              <span>
                <img src={stats.home_team_logo} alt={stats.home_team_shortcut}></img>
              </span>
              <span className="strong">vs</span>
              <span>
                <img src={stats.visitor_team_logo} alt={stats.visitor_team_shortcut}></img>
              </span>
            </div>
        </div>

        <div className="w3-margin">
          <div className="w3-section w3-row-padding w3-center">
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">Power Play %</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half w3-container" style={{color:stats.home_team_color}}>{stats.home_pp_pctg}</div>
                <div className="w3-half w3-container" style={{color:stats.visitor_team_color}}>{stats.visitor_pp_pctg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">Penalty Kill %</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half w3-container" style={{color:stats.home_team_color}}>{stats.home_pk_pctg}</div>
                <div className="w3-half w3-container" style={{color:stats.visitor_team_color}}>{stats.visitor_pk_pctg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">PDO</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half w3-container" style={{color:stats.home_team_color}}>{stats.home_pdo}</div>
                <div className="w3-half w3-container" style={{color:stats.visitor_team_color}}>{stats.visitor_pdo}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">Faceoff %</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half w3-container" style={{color:stats.home_team_color}}>{stats.home_fac_pctg}</div>
                <div className="w3-half w3-container" style={{color:stats.visitor_team_color}}>{stats.visitor_fac_pctg}</div>
              </div>
            </div>
          </div>

          <div className="w3-section w3-row-padding w3-center">
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">Goals For</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half w3-container" style={{color:stats.home_team_color}}>{stats.home_goals_for_pg}</div>
                <div className="w3-half w3-container" style={{color:stats.visitor_team_color}}>{stats.visitor_goals_for_pg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">Goals Against</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half w3-container" style={{color:stats.home_team_color}}>{stats.home_goals_against_pg}</div>
                <div className="w3-half w3-container" style={{color:stats.visitor_team_color}}>{stats.visitor_goals_against_pg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">Shots For</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half w3-container" style={{color:stats.home_team_color}}>{stats.home_shots_ongoal_for_pg}</div>
                <div className="w3-half w3-container" style={{color:stats.visitor_team_color}}>{stats.visitor_shots_ongoal_for_pg}</div>
              </div>
            </div>
            <div className="w3-quarter">
              <div className="w3-container pcolor w3-padding-small">Shots Against</div>
              <div className="w3-row w3-xlarge strong">
                <div className="w3-half w3-container" style={{color:stats.home_team_color}}>{stats.home_shots_ongoal_against_pg}</div>
                <div className="w3-half w3-container" style={{color:stats.visitor_team_color}}>{stats.visitor_shots_ongoal_against_pg}</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
