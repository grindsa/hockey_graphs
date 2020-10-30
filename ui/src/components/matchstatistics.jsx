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
        <HighchartsReact highcharts={Highcharts} options={this.props.options} immutable={true} />
      );
    }else{
      return (
        <ZoneChart options={this.props.options} />
      )
    }
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
