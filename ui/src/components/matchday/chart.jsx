import React, {useState, useEffect} from 'react';
import Highcharts from 'highcharts';
import HighchartsReact from 'highcharts-react-official';
import HighchartsMore from 'highcharts/highcharts-more';
import HighchartsExporting from 'highcharts/modules/exporting';
import Timeline from 'highcharts/modules/timeline.js';
import HighchartsOfflineExporting from "highcharts/modules/offline-exporting";
import Heatmap from 'highcharts/modules/heatmap.js';
import highchartsGantt from "highcharts/modules/gantt";
import { HeatmapJs } from './heatmapjs';
import { MatchOverview } from './matchoverview';
import { PreMatchOverview } from './prematchoverview';
import { PeriodSelector } from './periodselector';
import { createnoChartMessage } from '../localization.js';
import { isEmpty } from '../sharedfunctions.js';

// Load Highcharts modules
HighchartsExporting(Highcharts);
HighchartsOfflineExporting(Highcharts);
highchartsGantt(Highcharts);
HighchartsMore(Highcharts);
Timeline(Highcharts);
Heatmap(Highcharts);

export const Chart = (props) => {
  /* block to render chart moetection is done via chartoptions */
  if (!isEmpty(props.options) && props.options.ctype === 'gantt'){
    return (
      <div className="w3-border">
        <Gantt options={props.options} updates={props.updates}/>
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
  }else if (!isEmpty(props.options) && props.options.home_pdo && props.options.visitor_pdo){
    return(
      <PreMatchOverview options={props.options} />
    )
  }else{
    const nochartdata = createnoChartMessage(props.language)
    return (
      <div className="w3-padding-16 nodata w3-center">{nochartdata}</div>
    )
  }
}

const Gantt = (props) => {
  // gant chart
  const [chart, setChart] = useState(props.options);
  const handlePeriodChange = (event) => {
    // change period
    const newData = props.updates[event.target.value].data
    const newChart = Object.assign({}, chart, newData);
    setChart(newChart);
  }

  return (
    <div className="w3-border">
      <HighchartsReact highcharts={Highcharts} constructorType={"ganttChart"} options={chart} immutable={true} />
      <div className="w3-margin-bottom w3-center">
        <PeriodSelector data={props.updates} onChange={handlePeriodChange} />
      </div>
    </div>
  )
}
