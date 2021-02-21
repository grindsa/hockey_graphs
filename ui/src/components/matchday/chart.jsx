import React from 'react';
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
