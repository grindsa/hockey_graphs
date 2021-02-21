import React, {useState, useEffect} from 'react';
import PropTypes from "prop-types";

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
