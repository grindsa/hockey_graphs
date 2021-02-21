import React, {useState, useEffect} from 'react';
import PropTypes from "prop-types";
import { overviewClassnames } from './matchstatisticservice.js';

export const MatchOverview = ({options}) => {
  // matchoverview shoing shots, gols, toi and penalties
  const stats = options
  return(
    <table className="w3-table w3-border w3-centered">
      <tbody>
        <TableRow statname={stats.shotsOnGoal} leftvalue = {stats.home_team.shotsOnGoal} rightvalue = {stats.visitor_team.shotsOnGoal} leftwidth = {stats.home_team.shotsOnGoal_pctg} rightwidth = {stats.visitor_team.shotsOnGoal_pctg} />
        <TableRow statname={stats.saves} leftvalue = {stats.home_team.saves} rightvalue = {stats.visitor_team.saves} leftwidth = {stats.home_team.saves_pctg} rightwidth = {stats.visitor_team.saves_pctg} />
        <TableRow statname={stats.puckpossession} leftvalue = {stats.home_team.puckpossession} rightvalue = {stats.visitor_team.puckpossession} leftwidth = {stats.home_team.puckpossession_pctg} rightwidth = {stats.visitor_team.puckpossession_pctg} />
        <TableRow statname={stats.penaltyMinutes} leftvalue = {stats.home_team.penaltyMinutes} rightvalue = {stats.visitor_team.penaltyMinutes} leftwidth = {stats.home_team.penaltyMinutes_pctg} rightwidth = {stats.visitor_team.penaltyMinutes_pctg} />
        <TableRow statname={stats.powerplaymin} leftvalue = {stats.home_team.powerplaymin} rightvalue = {stats.visitor_team.powerplaymin} leftwidth = {stats.home_team.powerplaymin_pctg} rightwidth = {stats.visitor_team.powerplaymin_pctg} />
        <TableRow statname={stats.ppGoals} leftvalue = {stats.home_team.ppGoals} rightvalue = {stats.visitor_team.ppGoals} leftwidth = {stats.home_team.ppGoals_pctg} rightwidth = {stats.visitor_team.ppGoals_pctg} />
        <TableRow statname={stats.shGoals} leftvalue = {stats.home_team.shGoals} rightvalue = {stats.visitor_team.shGoals} leftwidth = {stats.home_team.shGoals_pctg} rightwidth = {stats.visitor_team.shGoals_pctg} />
        <TableRow statname={stats.faceOffsWon} leftvalue = {stats.home_team.faceOffsWon} rightvalue = {stats.visitor_team.faceOffsWon} leftwidth = {stats.home_team.faceOffsWon_pctg} rightwidth = {stats.visitor_team.faceOffsWon_pctg} />
      </tbody>
    </table>
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
