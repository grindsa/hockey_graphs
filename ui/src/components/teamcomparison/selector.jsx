import React from 'react';
import { isEmpty } from '../sharedfunctions.js';
import { createSelectOptions }  from './teamcomparisonstateservice.js';

export class Selector extends React.Component{
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
