import React, {useState, useEffect} from 'react';
import { isMobile } from 'react-device-detect';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import HighchartsMore from 'highcharts/highcharts-more';
import highchartsDumbbell from "highcharts/modules/dumbbell";
import HighchartsExporting from 'highcharts/modules/exporting';
import HighchartsOfflineExporting from "highcharts/modules/offline-exporting";
import AnnotationsModule from 'highcharts/modules/annotations';
import Heatmap from 'highcharts/modules/heatmap.js';
import { Comment } from './comment';
import { createTcSliderText, createnoChartMessage} from '../localization.js';

import Slider from 'rc-slider';
import 'rc-slider/assets/index.css';

// Load Highcharts modules
HighchartsExporting(Highcharts);
HighchartsOfflineExporting(Highcharts);
HighchartsMore(Highcharts);
Heatmap(Highcharts);
AnnotationsModule(Highcharts);
highchartsDumbbell(Highcharts);

export const Chart = (props) => {
  /* block to render chart mobile differenciation is done via chartoptions */

  const [slidervalue, setSlidervalue] = useState(Object.keys(props.options.updates).length);
  const [chart, setChart] = useState(props.options.chart);
  const [updates, setUpdates] = useState(props.options.updates)

  const handleSliderChange = async (newvalue) => {
    // update slidervalue after usage
    await setSlidervalue(newvalue)
    // update chart after sliderchange
    updateChart(updates[newvalue].chartoptions)
  }

  const updateChart = (newData) => {
    // update chart
    const newChart = Object.assign({}, chart, newData);
    setChart(newChart);
  }

  useEffect(() => {
    // this is a chart-change - we also need to reset slidervalue and updates "updates"
    setChart(props.options.chart)
    setSlidervalue(Object.keys(props.options.updates).length)
    setUpdates(props.options.updates)
  }, [props.options.chart])

  if (chart){
    // get the number of dataupdates as this will be the max-val for the slider
    const slidermaxval = Object.keys(props.options.updates).length
    const slidertext = createTcSliderText(props.language, slidervalue, slidermaxval)
    // const SliderWithTooltip = createSliderWithTooltip(Slider);
    var classNames = ""

    if (isMobile) {
      classNames = "w3-center w3-margin-left w3-margin-right"
    }
    return (
      <React.Fragment>
        <Slider
          min={1}
          max={slidermaxval}
          defaultValue={slidervalue}
          onChange={handleSliderChange}
          trackStyle={{ backgroundColor: '#999999', }}
          handleStyle={{
            borderColor: '#999999',
          }}
        />
        <div className="w3-center w3-margin-bottom">{slidertext}</div>
        <div className="w3-border">
          <HighchartsReact highcharts={Highcharts} options={chart} immutable={true}/>
        </div>
        <Comment text={props.options.comment} />
      </React.Fragment>
    )
  }else{
    const nochartdata = createnoChartMessage(props.language)
    return (
      <div className="w3-padding-16 nodata w3-center">{nochartdata}</div>
    )
  }
}
