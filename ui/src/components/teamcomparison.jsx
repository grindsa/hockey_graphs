import React from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import HighchartsMore from 'highcharts/highcharts-more';
import HighchartsExporting from 'highcharts/modules/exporting';
import HighchartsOfflineExporting from "highcharts/modules/offline-exporting";
import Heatmap from 'highcharts/modules/heatmap.js';
import Slider from 'react-rangeslider'
import 'react-rangeslider/lib/index.css'
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
      // get chart to be shown
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
  constructor(props) {
    super(props);
    this.state = props.options

    this.updateChart = this.updateChart.bind(this);
    this.handleSliderChange = this.handleSliderChange.bind(this);
  }

  componentDidMount(){
    // set initial slidervalue
    this.setState({slidervalue: Object.keys(this.props.options.updates).length});
  }

  updateChart(newData){
    // update chart in state
    this.setState(currentState => {
      return {
      ... currentState,
      chart: newData,
      }
    });
  }

  handleSliderChange(newvalue){
    // update slidervalue after usage 
    this.setState(currentState => {
      return {
      ... currentState,
      slidervalue: newvalue,
      }
    });
  }

  render() {
    if (this.state.chart){
      // get the number of dataupdates as this will be the max-val for the slider
      const slidermaxval = Object.keys(this.props.options.updates).length
      return (
        <React.Fragment>
          <Slider
            min={0}
            max={slidermaxval}
            value = {this.state.slidervalue}
            orientation='horizontal'
            onChange={this.handleSliderChange}
          />
          <div className="w3-border">
            <button  onClick={() => this.updateChart(this.state.updates[1].chartoptions)}>foo 1</button>
            <button  onClick={() => this.updateChart(this.state.updates[2].chartoptions)}>foo 2</button>
            <button  onClick={() => this.updateChart(this.state.updates[3].chartoptions)}>foo 3</button>
            <HighchartsReact highcharts={Highcharts} options={this.state.chart} />
          </div>
        </React.Fragment>
      )
    }else{
      const nochartdata = createnoChartMessage(this.props.language)
      return (
        <div className="w3-padding-16 nodata w3-center">{nochartdata}</div>
      )
    }
  }
}
