import React from 'react';
import { isEmpty } from '../sharedfunctions.js';
import ReactMarkdown from 'react-markdown'
import gfm from 'remark-gfm'

export class Comment extends React.Component{
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
