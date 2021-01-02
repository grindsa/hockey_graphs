import React from 'react';
import { isEmpty } from '../sharedfunctions.js';
import { createSelectOptions }  from './teamcomparisonstateservice.js';

export const Selector = ({stats, value, onChange}) => {
  if (isEmpty(stats)){
    return (<p></p>)
  }else{
    const optionList = createSelectOptions(stats)
    return (
      <div className="w3-center my-padding-4">
        <select className="w3-select w3-border selectbg" value={value} onChange={onChange}>
          {optionList}
        </select>
      </div>
    )
  }
}
