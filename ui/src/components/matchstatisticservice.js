import React from 'react';
import { isEmpty } from './sharedfunctions.js';

export const createTableHeader = function(data){
  /* create database header */
  if (data){
    var tableheader = data.th.map((th, index) =>{
      return(
        <th key={index} className={data.align[index]}>{th}</th>
      )
    });
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
        if (image){
          return(
            <td key={`td-${index}`}><img src={td} width='25' /></td>
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
