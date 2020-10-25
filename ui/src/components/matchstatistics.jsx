import React from 'react';
import { isMobile } from 'react-device-detect';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import HighchartsExporting from 'highcharts/modules/exporting'
import { createTableHeader, createTableBody, createSelectOptions } from './matchstatisticservice.js'
import { asyncGET, isEmpty } from './sharedfunctions.js';


// Load Highcharts modules
require("highcharts/modules/exporting")(Highcharts);

export class MatchStatistics extends React.Component {
  /* main component for matchstatistics */
  constructor(props) {
    super(props);
    if (props.match){
      this.state = {
        match: props.match,
        matchstatistics: []
      };
    }
  }

  async componentDidMount(){
    // get matchstatistics
    const matchstatistics = await asyncGET(this.props.matchstatistics + this.props.match.match_id + '?language=' + this.props.language)
    this.setState({matchstatistics: matchstatistics});
  }
  filterMatchStatistic(statlist){
    var matchstat = {}
    for (let stat of statlist){
      if (stat.display){
        matchstat = stat
        break;
      }
    }
    return matchstat
  }

  render() {
    /* filter statistic to be displayed */
    const MatchStatistic = this.filterMatchStatistic(this.state.matchstatistics)
    return (
      <React.Fragment>
      <MatchHeader match={this.props.match} reset={this.props.reset} />
      <Selector matches={this.state.matchstatistics}/>
      <Chart options={MatchStatistic.chart}/>
      <Table data={MatchStatistic.table}/>
      </React.Fragment>
    );
  }
}

class MatchHeader extends React.Component {
  /* render match header */
  render() {
    var home_team = this.props.match.home_team_name
    var visitor_team = this.props.match.visitor_team_name
    if (isMobile) {
      home_team = this.props.match.home_team_shortcut
      visitor_team = this.props.match.visitor_team_shortcut
    }
    return (
      <div className="w3-container w3-padding-small scolor w3-center">
        <h1>
          <span className="w3-padding-small pseudohead">{home_team}</span>
          <span className="w3-padding-small middle"><img src={this.props.match.home_team_logo} alt={this.props.match.home_team_shortcut} width="40px"/></span>
          <span className="w3-padding-small">{this.props.match.result}</span>
          <span className="w3-padding-small middle"><img src={this.props.match.visitor_team_logo} alt={this.props.match.visitor_team_logo} width="40px"/></span>
          <span className="w3-padding-small pseudohead">{visitor_team}</span>
          <span className="w3-padding-small"><i className="w3-margin-right w3-xxlarge fa fa-arrow-circle-o-left w3-right" onClick={() => this.props.reset()} /></span>
        </h1>
      </div>
    );
  }
}

class Selector extends React.Component{
  /* selector for different statistics */
  render(){
    if (isEmpty(this.props.matches)){
      return (<p></p>)
    }else{
      const [optionList, selectId] = createSelectOptions(this.props.matches)
      return (
        <div className="w3-container w3-padding-small w3-center">
        <select className="w3-select w3-border" defaultValue={selectId}>
          {optionList}
        </select>
        </div>
      )
    }
  }
}

class Chart extends React.Component{
  /* block to render chart */
  render() {
    return (
      <HighchartsReact highcharts={Highcharts} options={this.props.options} />
    );
  }
}

class Table extends React.Component{
  /* render table with data */
  render() {
    if (isEmpty(this.props.data)){
      return (<p></p>)
    }else{
      /* create table header and footer */
      const tableHeader = createTableHeader(this.props.data);
      const tableBody = createTableBody(this.props.data);
      return (
        <table className="w3-table w3-bordered w3-centered">
          <thead><tr className="scolor">{tableHeader}</tr></thead>
          <tbody>{tableBody}</tbody>
        </table>
      );
    }
  }
}
