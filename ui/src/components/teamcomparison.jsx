import React from 'react';
import { isMobile } from 'react-device-detect';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import HighchartsMore from 'highcharts/highcharts-more';
import HighchartsExporting from 'highcharts/modules/exporting';
import HighchartsOfflineExporting from "highcharts/modules/offline-exporting";
import AnnotationsModule from 'highcharts/modules/annotations';
import Heatmap from 'highcharts/modules/heatmap.js';
import ReactMarkdown from 'react-markdown'
import Slider from 'react-rangeslider'
import gfm from 'remark-gfm'
// import 'react-rangeslider/lib/index.css'
import '../css/slider.css';
import { checkTcUpdate, createSelectOptions }  from './teamcomparison/teamcomparisonstateservice.js';
import { asyncGET, isEmpty } from './sharedfunctions.js';
import { createnostatMessage, createTcSliderText } from './localization.js';

// Load Highcharts modules
HighchartsExporting(Highcharts);
HighchartsOfflineExporting(Highcharts);
HighchartsMore(Highcharts);
Heatmap(Highcharts);
AnnotationsModule(Highcharts);


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
      const tcdic = await asyncGET(this.props.teamcomparison + '?season=' + this.props.season + '&mobile=' + isMobile + '&language=' + this.props.language)
      this.setState({teamcomparisonList: tcdic});
    }
  }

  async componentDidUpdate(prevProps) {
    /* we get the url to fectch as props and monitor it here */
    const tcupdate = checkTcUpdate(this.props.teamcomparison, prevProps.teamcomparison, this.props.season, prevProps.season, this.props.language, prevProps.language)
    if (tcupdate){
        // get team comparison
        const tcdic = await asyncGET(this.props.teamcomparison + '?season=' + this.props.season + '&mobile=' + isMobile + '&language=' + this.props.language)
        this.setState({teamcomparisonList: tcdic});
    }
  }

  handleStatChange(event){
    const newvalue = event.target.value
    if (this.state.selectedstat !== newvalue){
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

class Comment extends React.Component{
  /* selector for different statistics */
  render(){
    if (isEmpty(this.props.text)){
      return (<p></p>)
    }else{
      return (
        <div className="w3-container">
          <ReactMarkdown source={this.props.text} plugins={[gfm]} />
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

  componentDidUpdate(prevProps){
    if (prevProps.options !== this.props.options){
      this.setState(this.props.options);
      // set initial slidervalue
      this.setState({slidervalue: Object.keys(this.props.options.updates).length});
    }
  }

  updateChart(newData){
    // update chart in state
    const newChart = Object.assign({}, this.state.chart, newData)
    this.setState({chart: newChart });
  }

  async handleSliderChange(newvalue){
    // update slidervalue after usage
    await this.setState(currentState => {
      return {
      ... currentState,
      slidervalue: newvalue,
      }
    });
    this.updateChart(this.state.updates[this.state.slidervalue].chartoptions)
  }

  render() {
    if (this.state.chart){
      // get the number of dataupdates as this will be the max-val for the slider
      const slidermaxval = Object.keys(this.props.options.updates).length
      const slidertext = createTcSliderText(this.props.language, this.state.slidervalue, slidermaxval)
      var className = ""

      if (isMobile) {
        var classNames = "w3-center w3-margin-left w3-margin-right"
      }

      return (
        <React.Fragment>
          <Slider
            min={1}
            max={slidermaxval}
            value = {this.state.slidervalue}
            step={1}
            orientation='horizontal'
            onChange={this.handleSliderChange}
            className={classNames}
          />
          <div className="w3-center w3-margin-bottom">{slidertext}</div>
          <div className="w3-border">
            <HighchartsReact highcharts={Highcharts} options={this.state.chart} immutable={true}/>
          </div>
          <Comment text={this.props.options.comment} />
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
