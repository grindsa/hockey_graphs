import React from 'react';
import { isMobile } from 'react-device-detect';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import HighchartsMore from 'highcharts/highcharts-more';
import HighchartsExporting from 'highcharts/modules/exporting';
import HighchartsOfflineExporting from "highcharts/modules/offline-exporting";
import AnnotationsModule from 'highcharts/modules/annotations';
import Heatmap from 'highcharts/modules/heatmap.js';

import Slider from 'react-rangeslider'
import '../../css/slider.css';
import { Comment } from './comment';
import { createTcSliderText, createnoChartMessage} from '../localization.js';

// Load Highcharts modules
HighchartsExporting(Highcharts);
HighchartsOfflineExporting(Highcharts);
HighchartsMore(Highcharts);
Heatmap(Highcharts);
AnnotationsModule(Highcharts);

export class Chart extends React.Component{
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
