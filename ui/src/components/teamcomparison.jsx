import React from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import HighchartsMore from 'highcharts/highcharts-more';
import HighchartsExporting from 'highcharts/modules/exporting';
import HighchartsOfflineExporting from "highcharts/modules/offline-exporting";
import Heatmap from 'highcharts/modules/heatmap.js';
import { checkTcUpdate, createSelectOptions }  from './teamcomparison/teamcomparisonstateservice.js';
import { asyncGET, isEmpty } from './sharedfunctions.js';
import { createnostatMessage } from './localization.js';

// Load Highcharts modules
HighchartsExporting(Highcharts);
HighchartsOfflineExporting(Highcharts);
HighchartsMore(Highcharts);
Heatmap(Highcharts);

export class TeamComparison extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      teamcomparisonList: [],
      selectedstat: 0,
    };

    this.handleStatChange = this.handleStatChange.bind(this);
  }

  async componentDidMount(){
    if (this.props.teamcomparison && this.props.season) {
      // get team comparison
      const matchdaydic = await asyncGET(this.props.teamcomparison + '?season=' + this.props.season)
      this.setState({teamcomparisonList: matchdaydic});
    }
  }

  async componentDidUpdate(prevProps) {
    /* we get the url to fectch as props and monitor it here */
    const tcupdate = checkTcUpdate(this.props.teamcomparison, prevProps.teamcomparison, this.props.season, prevProps.season)
    if (tcupdate){
        // get team comparison
        const tcdic = await asyncGET(this.props.teamcomparison + '?season=' + this.props.season)
        this.setState({teamcomparisonList: tcdic});
    }
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
    const nostatmessage = createnostatMessage(this.props.language)
    if (!isEmpty(this.state.teamcomparisonList)){
      const chart = this.state.teamcomparisonList[this.state.selectedstat]
      return (
        <React.Fragment>
          <Selector stats={this.state.teamcomparisonList}  onChange={this.handleStatChange} value={this.state.selectedstat} />
          <Chart options={chart} language={this.props.language} />
        </React.Fragment>
      )
    }else{
      return (
          <div className="w3-padding-16 w3-center">{nostatmessage}</div>
      )
    }
  }
}

class Selector extends React.Component{
  /* selector for different statistics */
  render(){
    if (isEmpty(this.props.stats)){
      return (<p></p>)
    }else{
      const optionList = createSelectOptions(this.props.stats)
      return (
        <div className="w3-center my-padding-4">
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
          <HighchartsReact highcharts={Highcharts} options={this.props.options.chart} immutable={true} />
        </div>
      )
    }else{
      const nochartdata = createnoChartMessage(this.props.language)
      return (
        <div className="w3-padding-16 nodata w3-center">{nochartdata}</div>
      )
    }
  }
}
