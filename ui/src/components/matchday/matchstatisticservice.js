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

export const overviewClassnames = function(leftValue, rightValue){
  /* specify classes for matchstat overview compare shots/gols/pp */
  let leftcolor
  let rightcolor
  if (leftValue === 0 && rightValue !== 0){
    /*  cases like ppgoal visitor_team) */
    leftcolor = ''
    rightcolor = ' pcolor'
  }else if (leftValue !== 0 && rightValue === 0){
    /*  cases like ppgoal home_team) */
    leftcolor = ' pcolor'
    rightcolor = ''
  }else if (leftValue === 0 && rightValue === 0){
    /* both values */
    leftcolor = ''
    rightcolor = ''
  }else if(leftValue === rightValue) {
    /* equal values but not zero */
    leftcolor = ' scolor'
    rightcolor = ' scolor'
  }else if(leftValue > rightValue) {
    /* home team has better value than visitor */
    leftcolor = ' pcolor'
    rightcolor = ' scolor'
  }else{
    /* vistior team does better than home_team */
    leftcolor = ' scolor'
    rightcolor = ' pcolor'
  }
  /* final classnames */
  var leftClassNames = 'w3-container w3-right-align w3-right' + leftcolor
  var rightClassNames = 'w3-container w3-left-align' + rightcolor

 return [leftClassNames, rightClassNames]
}
