import React from 'react';
import { isEmpty } from '../sharedfunctions.js';

export const createTableHeader = function(data){
  /* create database header */
  if (data){
    if(data.tooltip){
      var tableheader = data.th.map((th, index) =>{
        return(
          <th key={index} className="w3-tooltip {data.align[index]}">{th} <span className="w3-text w3-tag w3-round-xlarge mytooltip pcolor">{data.tooltip[index]}</span></th>
        )
      });
    }else{
      var tableheader = data.th.map((th, index) =>{
        return(
          <th key={index} className="w3-tooltip {data.align[index]}">{th}</th>
        )
      });
    }
  }else{
    var tableheader = null;
  }
  return tableheader
}

export const createTableBody = function(data){
  /* create database header */
  if (data){
    var tablebody = data.td.map((tr, index) =>{
      var trow = tr.map((td, index) =>{
        const image = td.toString().includes("img")
        const badge = td.toString().includes("w3-badge line")
        if (image){
          return(
            <td key={`td-${index}`}><img src={td} width='25' /></td>
          )
        }else if(badge){
          var value =td.replace("w3-badge line", "");
          return(
            <td key={`td-${index}`}><span className={td}>{value}</span></td>
          )
        }else{
          return(
            <td  key={`td-${index}`} className={data.align[index]}>{td}</td>
          )
        }
      });
      return(
        <tr key={index}>{trow}</tr>
      )
    });
  }else{
    var tablebody = null;
  }
  return tablebody
}

export const createSelectOptions = function(data){
  /* create option header */
  var optionlist = data.map((option, index) => {
    return(
      <option value={index} key={`option-${index}`}> {option.title} </option>
    )
  });
  return optionlist
}

export const overviewClassnames = function(leftValue, rightValue){
  /* specify classes for matchstat overview*/

  if (leftValue === 0 && rightValue !== 0){
    /*  cases like ppgoal visitor_team) */
    var leftcolor = ''
    var rightcolor = ' pcolor'
  }else if (leftValue !== 0 && rightValue === 0){
    /*  cases like ppgoal home_team) */
    var leftcolor = ' pcolor'
    var rightcolor = ''
  }else if (leftValue === 0 && rightValue === 0){
    /* both values */
    var leftcolor = ''
    var rightcolor = ''
  }else if(leftValue === rightValue) {
    /* equal values but not zero */
    var leftcolor = ' scolor'
    var rightcolor = ' scolor'
  }else if(leftValue > rightValue) {
    /* home team has better value than visitor */
    var leftcolor = ' pcolor'
    var rightcolor = ' scolor'
  }else{
    /* vistior team does better than home_team */
    var leftcolor = ' scolor'
    var rightcolor = ' pcolor'
  }
  /* final classnames */
  var leftClassNames = 'w3-container w3-right-align w3-right' + leftcolor
  var rightClassNames = 'w3-container w3-left-align' + rightcolor

 return [leftClassNames, rightClassNames]
}

export const createnostatMessage = function(language){
  /* build no message based on language setting */
  if (language == 'DE'){
    var nostatmessage = 'Keine Statistiken verfügbar'
  }else{
    var nostatmessage = 'No statistics available.'
  }
  return nostatmessage
}

export const createnoChartMessage = function(language){
  /* build no message based on language setting */
  if (language == 'DE'){
    var nostatmessage = 'Keine Daten verfügbar.'
  }else{
    var nostatmessage = 'No data to render chart.'
  }
  return nostatmessage
}
