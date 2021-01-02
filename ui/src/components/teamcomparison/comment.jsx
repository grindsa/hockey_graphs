import React from 'react';
import { isEmpty } from '../sharedfunctions.js';
import ReactMarkdown from 'react-markdown'
import gfm from 'remark-gfm'

export const Comment = ({text}) => {
  if (isEmpty(text)){
    return (<p></p>)
  }else{
    return (
      <div className="w3-container">
          <ReactMarkdown source={text} plugins={[gfm]} />
      </div>
    )
  }
}
