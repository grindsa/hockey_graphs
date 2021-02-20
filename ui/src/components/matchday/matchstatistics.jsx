import React, {useState, useEffect} from 'react';
import PropTypes from "prop-types";
import { isMobileOnly } from 'react-device-detect';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import HighchartsMore from 'highcharts/highcharts-more';
import HighchartsExporting from 'highcharts/modules/exporting';
import HighchartsOfflineExporting from "highcharts/modules/offline-exporting";
import Timeline from 'highcharts/modules/timeline.js';
import Heatmap from 'highcharts/modules/heatmap.js';
import highchartsGantt from "highcharts/modules/gantt";
import { HeatmapJs } from './heatmapjs'
import { createTableHeader, createTableBody, createSelectOptions, overviewClassnames } from './matchstatisticservice.js'
import { asyncGET, isEmpty } from '../sharedfunctions.js';
import { createnoChartMessage } from '../localization.js';
import { navigate } from "hookrouter";

// Load Highcharts modules
HighchartsExporting(Highcharts);
HighchartsOfflineExporting(Highcharts);
highchartsGantt(Highcharts);
HighchartsMore(Highcharts);
Timeline(Highcharts);
Heatmap(Highcharts);

export const MatchStatistics = (props) => {
  /* main component for matchstatistics */
  // const [match, setMatch] = useState(props.match)
  const [matchstatistics, setMatchstatistics] = useState([])
  const [selectedstat, setSelectedstat] = useState(0)

  const handleStatChange = (event) => {
    const newValue = event.target.value
    if (selectedstat !== newValue){
      setSelectedstat(newValue)
      const linkValue = parseInt(newValue) + 1
      navigate('/matchstatistics/' + props.season + '/' + props.match['match_id'] + '/' + linkValue);
    }
  }

  useEffect(() => {
    if (props.matchstatistics && props.language) {
      const ms_get = async () => {
        const matchstatistics = await asyncGET(props.matchstatistics + props.match.match_id+ '?language=' + props.language  + '&mobile=' + isMobileOnly)
        if (!isEmpty(matchstatistics)){
          setMatchstatistics(matchstatistics);
        }
      }
      ms_get()
    }
  }, [props.matchstatistics, props.language])

  if (props.stat && props.stat != selectedstat + 1){
      setSelectedstat(props.stat - 1)
  }

  const MatchStatistic = matchstatistics[selectedstat]
  if (!isEmpty(MatchStatistic)){
    return (
      <React.Fragment>
        <MatchHeader match={props.match} reset={props.reset} />
        <Selector matches={matchstatistics}  onChange={handleStatChange} value={selectedstat}/>
        <MatchData language={props.language} chart={MatchStatistic.chart} table={MatchStatistic.table} match={props.match} tabs={MatchStatistic.tabs}/>
      </React.Fragment>
    );
  }else{
    // const nostatmessage = createnostatMessage(props.language)
    return (
      <React.Fragment>
        <MatchHeader match={props.match} reset={props.reset} />
      </React.Fragment>
    )
  }
}

const MatchData = (props) => {
  // matchdata
  const [activeTab, setActiveTab] = useState(0)
  const switchTab = (newIndex) => {
    setActiveTab(newIndex)
  };

  let home_format
  let visitor_format
  if(props.tabs){
    if (activeTab === 0){
      home_format = "w3-col tablink w3-bottombar tab-red w3-hover-light-grey w3-padding my-half"
      visitor_format = "w3-col tablink w3-bottombar w3-hover-light-grey w3-padding my-half"
    }else{
      visitor_format = "w3-col tablink w3-bottombar tab-red w3-hover-light-grey w3-padding my-half"
      home_format = "w3-col tablink w3-bottombar w3-hover-light-grey w3-padding my-half"
    }

    return (
      <React.Fragment>
        <div className="w3-row">
          <div className ={home_format} onClick={() => switchTab(0)}>{props.match.home_team_name}</div>
          <div className ={visitor_format} onClick={() => switchTab(1)}>{props.match.visitor_team_name}</div>
        </div>
        <Chart options={props.chart[activeTab]} language={props.language} />
        <Table data={props.table[activeTab]} />
      </React.Fragment>
    )
  }else{
    return (
      <React.Fragment>
        <Chart options={props.chart} language={props.language} />
        <Table data={props.table} />
      </React.Fragment>
    );
  }
}

const MatchHeader = (props) => {
  /* render match header */
  var home_team = props.match.home_team_name
  var visitor_team = props.match.visitor_team_name
  if (isMobileOnly) {
    home_team = props.match.home_team_shortcut
    visitor_team = props.match.visitor_team_shortcut
  }
  return (
    <div className="w3-container w3-row middle scolor pseudohead matchheader">
      <div className="w3-col" style={{width:'40%'}}>
        <img src={props.match.home_team_logo} className="middle w3-right" alt={props.match.home_team_shortcut} width="40px"/>
        <span className="my-padding-8 w3-margin-right w3-right">{home_team}</span>
      </div>
      <div className="w3-col w3-center" style={{width:'20%'}}><span className="w3-tag pcolor w3-border w3-round my-padding-4">{props.match.result}</span></div>
      <div className="w3-col" style={{width:'40%'}}>
        <img src={props.match.visitor_team_logo} className="middle w3-left" alt={props.match.visitor_team_logo} width="40px"/>
        <span className="my-padding-8 w3-margin-left w3-left">{visitor_team}</span>
        <i className="my-padding-8 w3-margin-right w3-large fa fa-arrow-alt-circle-left w3-right" onClick={() => props.reset()} />
      </div>
    </div>
  );
}

MatchHeader.propTypes = {
    match: PropTypes.object,
    reset: PropTypes.func.isRequired,
};

const Selector = (props) => {
  /* selector for different statistics */
  if (isEmpty(props.matches)){
    return (<p></p>)
  }else{
    const optionList = createSelectOptions(props.matches)
    return (
      <div className="w3-center my-padding-4">
      <select className="w3-select w3-border selectbg" value={props.value} onChange={props.onChange}>
        {optionList}
      </select>
      </div>
    )
  }
}

const Chart = (props) => {
  /* block to render chart moetection is done via chartoptions */
  if (!isEmpty(props.options) && props.options.ctype === 'gantt'){
    return (
      <div className="w3-border">
        <HighchartsReact highcharts={Highcharts} constructorType={"ganttChart"} options={props.options} immutable={true} />
      </div>
    )
  }else if (!isEmpty(props.options) && props.options.chart){
    return (
      <div className="w3-border">
        <HighchartsReact highcharts={Highcharts} options={props.options} immutable={true} />
      </div>
    )
  }else if (!isEmpty(props.options)  && props.options.shotsOnGoal){
    return(
      <MatchOverview options={props.options} />
    )
  }else if (!isEmpty(props.options) && props.options.leftlabel){
    return(
      <HeatmapJs data={props.options} />
    )
  }else{
    const nochartdata = createnoChartMessage(props.language)
    return (
      <div className="w3-padding-16 nodata w3-center">{nochartdata}</div>
    )
  }
}

const MatchOverview = ({options}) => {
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

const Table = ({data}) => {
  /* render table with data */
  if (isEmpty(data)){
    return (<p></p>)
  }else{
    /* create table header and footer */
    const tableHeader = createTableHeader(data);
    const tableBody = createTableBody(data);
    return (
      <table className="w3-table w3-bordered w3-centered">
        <thead><tr className="scolor">{tableHeader}</tr></thead>
        <tbody>{tableBody}</tbody>
      </table>
    );
  }
}
