import React from 'react';
import { isMobile } from 'react-device-detect';
import Highcharts from 'highcharts'
import HighchartsReact from 'highcharts-react-official'
import HighchartsMore from 'highcharts/highcharts-more';
import HighchartsExporting from 'highcharts/modules/exporting'
import { createTableHeader, createTableBody, createSelectOptions, overviewClassnames } from './matchstatisticservice.js'
import { asyncGET, isEmpty } from './sharedfunctions.js';

// Load Highcharts modules
require("highcharts/modules/exporting")(Highcharts);
HighchartsMore(Highcharts);


export class MatchStatistics extends React.Component {
  /* main component for matchstatistics */
  constructor(props) {
    super(props);
    if (props.match){
      this.state = {
        match: props.match,
        matchstatistics: [],
        selectedstat: 0,
      };
    }
    this.handleStatChange = this.handleStatChange.bind(this);
  }

  async componentDidMount(){
    // get matchstatistics
    const matchstatistics = await asyncGET(this.props.matchstatistics + this.props.match.match_id + '?language=' + this.props.language)
    this.setState({matchstatistics: matchstatistics})
  }

  handleStatChange(event){
    const newvalue = event.target.value
    if (this.state.selectedMatch !== newvalue){
      this.setState(currentState => {
        return {
        ... currentState,
        selectedstat: newvalue,
        }
      });
    }
  }

  render() {
    const MatchStatistic = this.state.matchstatistics[this.state.selectedstat]
    if (!isEmpty(MatchStatistic)){
      return (
        <React.Fragment>
          <MatchHeader match={this.props.match} reset={this.props.reset} />
          <Selector matches={this.state.matchstatistics}  onChange={this.handleStatChange} value={this.state.selectedstat}/>
          <MatchData chart={MatchStatistic.chart} table={MatchStatistic.table} match={this.props.match} tabs={MatchStatistic.tabs}/>
        </React.Fragment>
      );
    }else{
      return (<p></p>)
    }
  }
}

class MatchData extends React.Component {
  constructor(props){
    super(props);
    this.state = {
        activeTab: 0,
    }
    this.switchTab = this.switchTab.bind(this);
  }

  switchTab(newIndex){
    this.setState({
      activeTab: newIndex
    })
  };

  render(){
    if(this.props.tabs){
      if (this.state.activeTab === 0){
        var home_format = "w3-col tablink w3-bottombar tab-red w3-hover-light-grey w3-padding my-half"
        var visitor_format = "w3-col tablink w3-bottombar w3-hover-light-grey w3-padding my-half"
      }else{
        var visitor_format = "w3-col tablink w3-bottombar tab-red w3-hover-light-grey w3-padding my-half"
        var home_format = "w3-col tablink w3-bottombar w3-hover-light-grey w3-padding my-half"
      }
      return (
        <React.Fragment>
          <div className="w3-row">
            <div className ={home_format} onClick={() => this.switchTab(0)}>{this.props.match.home_team_name}</div>
            <div className ={visitor_format} onClick={() => this.switchTab(1)}>{this.props.match.visitor_team_name}</div>
          </div>
          <Chart options={this.props.chart[this.state.activeTab]} />
          <Table data={this.props.table[this.state.activeTab]} />
        </React.Fragment>
      )
    }else{
      return (
        <React.Fragment>
          <Chart options={this.props.chart} />
          <Table data={this.props.table} />
        </React.Fragment>
      );
    }
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
        <div className="w3-container w3-row middle scolor pseudohead w3-padding">
          <div className="w3-col" style={{width:'45%'}}>
            <span className="w3-padding-small w3-right"><span className="w3-padding-small">{home_team}</span><img src={this.props.match.home_team_logo} className="middle" alt={this.props.match.home_team_shortcut} width="40px"/></span>
          </div>
          <div className="w3-col w3-center w3-padding-top" style={{width:'10%'}}>{this.props.match.result}</div>
          <div className="w3-col" style={{width:'45%'}}>
            <span className="w3-padding-small w3-left"><img src={this.props.match.visitor_team_logo} className="middle" alt={this.props.match.visitor_team_logo} width="40px"/><span className="w3-padding-small">{visitor_team}</span></span>
            <i className="w3-padding-top w3-margin-right w3-xlarge fa fa-arrow-circle-o-left w3-right" onClick={() => this.props.reset()} />
          </div>
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
      const optionList = createSelectOptions(this.props.matches)
      return (
        <div className="w3-container w3-padding-small w3-center">
        <select className="w3-select w3-border selectbg" value={this.props.value} onChange={this.props.onChange}>
          {optionList}
        </select>
        </div>
      )
    }
  }
}

class Chart extends React.Component{
  /* block to render chart mobile differenciation is done via chartoptions */
  render() {
    if (this.props.options.chart){
      return (
        <div className="w3-border">
          <HighchartsReact highcharts={Highcharts} options={this.props.options} immutable={true} />
        </div>
      )
    }else if (this.props.options.home_team){
      return(
        <MatchOverview options={this.props.options} />
      )
    }else{
      return (
        <ZoneChart options={this.props.options} />
      )
    }
  }
}

class MatchOverview extends React.Component{
    render(){
      const stats = this.props.options
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
}

class TableRow extends React.Component {
  /* single row in matchstats we need to assing color classes based on values */
  render(){
    var [leftClassNames, rightClassNames] = overviewClassnames(this.props.leftvalue, this.props.rightvalue)
    return (
      <React.Fragment>
        <tr><td colSpan="2" className="w3-small"><b>{this.props.statname}</b></td></tr>
        <tr>
            <td style={{width:'50%'}}><div className="w3-container w3-light-grey w3-tiny nopadding"><div className={leftClassNames} style={{width:this.props.leftwidth}}>{this.props.leftvalue}</div></div></td>
            <td style={{width:'50%'}}><div className="w3-container w3-light-grey w3-tiny nopadding"><div className={rightClassNames} style={{width:this.props.rightwidth}}>{this.props.rightvalue}</div></div></td>
        </tr>
      </React.Fragment>
    )
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

class ZoneChart extends React.Component{
  /* render table with data differenciation if mobile or not */
  render() {
    if (isMobile) {
      var img_width = 30
      var shotzone_classes = "shotzone_mobile"
    } else{
      var img_width = 50
      var shotzone_classes = "shotzone"
    }
    return (
      <div className="w3-display-container w3-margin">
        <img src={this.props.options.background_image} alt="shoot-zones" style={{width:"100%"}} />
        <div className="w3-display-left w3-container">
           <div className="w3-margin"><img className="w3-padidng-small middle" src={this.props.options.home_team.logo} alt="logo" width={img_width} /> <span className={shotzone_classes}>{ this.props.options.home_team.left.roundpercent }%</span></div>
           <div className="w3-margin"><img className="w3-padidng-small middle" src={this.props.options.visitor_team.logo} alt="logo" width={img_width} /> <span className={shotzone_classes}>{ this.props.options.visitor_team.left.roundpercent }%</span></div>
        </div>
        <div className="w3-display-middle w3-container">
          <div className="w3-margin"><img className="w3-padidng-small middle" src={this.props.options.home_team.logo} alt="logo" width={img_width} /> <span className={shotzone_classes}>{ this.props.options.home_team.slot.roundpercent }%</span></div>
          <div className="w3-margin"><img className="w3-padidng-small middle" src={this.props.options.visitor_team.logo} alt="logo" width={img_width} /> <span className={shotzone_classes}>{ this.props.options.visitor_team.slot.roundpercent }%</span></div>
        </div>
        <div className="w3-display-right w3-container">
          <div className="w3-margin"><img className="w3-padidng-small middle" src={this.props.options.home_team.logo} alt="logo" width={img_width} /> <span className={shotzone_classes}>{ this.props.options.home_team.right.roundpercent }%</span></div>
          <div className="w3-margin"><img className="w3-padidng-small middle" src={this.props.options.visitor_team.logo} alt="logo" width={img_width} /> <span className={shotzone_classes}>{ this.props.options.visitor_team.right.roundpercent }%</span></div>
        </div>
        <div className="w3-display-bottommiddle w3-container">
          <div className="w3-margin"><img className="w3-padidng-small middle" src={this.props.options.home_team.logo} alt="logo" width={img_width} /> <span className={shotzone_classes}>{ this.props.options.home_team.blue_line.roundpercent }%</span></div>
          <div className="w3-margin"><img className="w3-padidng-small middle" src={this.props.options.visitor_team.logo} alt="logo" width={img_width} /> <span className={shotzone_classes}>{ this.props.options.visitor_team.blue_line.roundpercent }%</span></div>
        </div>
      </div>
    );
  }
}
