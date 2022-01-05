import ReactDOM, { render } from 'react-dom';
import React, {useState, useEffect} from 'react';
import { PeriodSelector } from './periodselector';
import { isEmpty, getParams } from '../sharedfunctions.js';
import { isMobileOnly } from 'react-device-detect';
import h337 from 'heatmap.js'

export const HeatmapJs = ({data, title}) => {

  if (isMobileOnly){
    var headline_classes = 'jsheadmap_headline_mobile w3-margin-top'
    var subheadline_classes = 'jsheadmap_subheadline_mobile'
    var canvas_classes = 'w3-margin-top w3-margin-right jsheatmap_mobile w3-display-container'
    var tag_name = '.jsheatmap_mobile'
    var img_size = 19
    var radius = 19
    var home_logo_classes = 'w3-display-left jsheatmap_homelogo_mobile'
    var visitor_logo_classes = 'w3-display-right jsheatmap_visitorlogo_mobile'
    var left_text_classes = 'w3-left jsheatmap_lefttext_mobile'
    var right_text_classes = 'w3-right jsheatmap_rightext_mobile'

  }else{
    var headline_classes = 'jsheadmap_headline w3-margin-top'
    var subheadline_classes = 'jsheadmap_subheadline'
    var canvas_classes = 'w3-margin-top w3-margin-right jsheatmap w3-display-container'
    var tag_name = '.jsheatmap'
    var img_size = 35
    var radius = 40
    var home_logo_classes = 'w3-display-left jsheatmap_homelogo'
    var visitor_logo_classes = 'w3-display-right jsheatmap_visitorlogo'
    var left_text_classes = 'w3-left jsheatmap_lefttext'
    var right_text_classes = 'w3-right jsheatmap_rightext'
  }

  // let _cfg = {'radius': radius, gradient: { 0.55: "rgb(77,123,187)", 0.7: "rgb(239,218,226)", 0.8: "rgb(224,184,200)", 0.9: "rgb(210,148,172)", 0.95: "rgb(194,112,145)", 1.0: "rgb(180,77,117)"}}
  let _cfg = {'radius': radius}
  let heatmapInstance = null

  useEffect(() => {
    _cfg.container = document.querySelector(tag_name);
    heatmapInstance = h337.create(_cfg)
    heatmapInstance.setData( data['data'][5] );
  }, [data])

  const handlePeriodChange = (event) => {
    // change period
    heatmapInstance.setData( data['data'][event.target.value] );
  }

  return (
    <div className="w3-container w3-center w3-border">
      <div className={headline_classes}>{data.title}</div>
      <div className={subheadline_classes}>{data.subtitle}</div>
      <PeriodSelector data={data.data} onChange={handlePeriodChange} />
      <div className={canvas_classes}>
          <div className={home_logo_classes}><img src={data.home_team_logo} width={img_size} height={img_size}></img></div>
          <div className={visitor_logo_classes}><img src={data.visitor_team_logo}  width={img_size} height={img_size}></img></div>
      </div>
      <div>
        <div className={left_text_classes}>{data.leftlabel}</div>
        <div className={right_text_classes}>{data.rightlabel}</div>
      </div>
      <div className="cpr">@2022 GrindSa <a href="https://hockeygraphs.dynamop.de">(https://hockeygraphs.dynamop.de)</a></div>
    </div>
  )
}
