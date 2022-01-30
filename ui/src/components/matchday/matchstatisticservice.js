import React from 'react';

export const createTableHeader = function(data){
  /* create database header */
  let tableheader
  if (data){
    if(data.tooltip){
      tableheader = data.th.map((th, index) =>{
        return(
          <th key={index} className="w3-tooltip {data.align[index]}">{th} <span className="w3-text w3-tag w3-round-xlarge mytooltip pcolor">{data.tooltip[index]}</span></th>
        )
      });
    }else{
      tableheader = data.th.map((th, index) =>{
        return(
          <th key={index} className="w3-tooltip {data.align[index]}">{th}</th>
        )
      });
    }
  }else{
    tableheader = null;
  }
  return tableheader
}

export const createTableBody = function(data){
  /* create bopdy */
  let tablebody
  if (data){
    tablebody = data.td.map((tr, index) =>{
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
    tablebody = null;
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

export const overviewClassnames = function(leftValue, rightValue, colors){
  /* specify classes for matchstat overview compare shots/gols/pp */
  let leftcolor
  let rightcolor
  if (leftValue === 0 && rightValue !== 0){
    /*  cases like ppgoal visitor_team) */
    leftcolor = ''
    rightcolor = colors.visitor_team_color_lead
  }else if (leftValue !== 0 && rightValue === 0){
    /*  cases like ppgoal home_team) */
    leftcolor = colors.home_team_color_lead
    rightcolor = ''
  }else if (leftValue === 0 && rightValue === 0){
    /* both values */
    leftcolor = ''
    rightcolor = ''
  }else if(leftValue === rightValue) {
    /* equal values but not zero */
    leftcolor = colors.home_team_color_lead
    rightcolor = colors.visitor_team_color_lead
  }else if(leftValue > rightValue) {
    /* home team has better value than visitor */
    leftcolor = colors.home_team_color_lead
    rightcolor = colors.visitor_team_color_behind
  }else{
    /* vistior team does better than home_team */
    leftcolor = colors.home_team_color_behind
    rightcolor = colors.visitor_team_color_lead
  }

  /* final classnames */
  // var leftClassNames = 'w3-container w3-right-align w3-right' + leftcolor
  // var rightClassNames = 'w3-container w3-left-align' + rightcolor
  var leftClassNames = 'w3-container w3-right-align w3-right'
  var rightClassNames = 'w3-container w3-left-align'

 return [leftClassNames, rightClassNames, leftcolor, rightcolor]
}
