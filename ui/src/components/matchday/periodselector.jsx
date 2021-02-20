import ReactDOM, { render } from 'react-dom';
import React from 'react';
import { getParams } from '../sharedfunctions.js';
import { isMobileOnly } from 'react-device-detect';

export const PeriodSelector = ({data, onChange}) => {

  if (isMobileOnly){
    var label_classes = 'mobile'
  } else {
    var label_classes = ''
  }

  // filter url parameters to check if we have skip the period header
  const params = getParams(window.location)
  if (params.disableperiod){
    // return nothing
    return(null)
  } else {
    // return period header
    // const period = periodList(data, label_classes, onChange)
    // console.log(period)
    return (
      <div className="w3-margin-top">
      {
        Object.keys(data).map((key, index) => (
          <React.Fragment key={`${index}-option`}><input className="w3-margin-left middle" type="radio" name="period" value={key} onChange={onChange} defaultChecked={data[key]['checked']} /><label className={label_classes}> {data[key]['name']}</label></React.Fragment>
        ))
      }
      </div>
    )
  }
}
