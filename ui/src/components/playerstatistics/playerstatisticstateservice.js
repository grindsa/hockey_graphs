import React from 'react';

export const checkTcUpdate = function(tcomparison, prevtcomparison, season, prevseason, lang, prevlang){
  /* this is to check if we have to fetch data from rest */
  var mupdate = false
  if (tcomparison !== prevtcomparison && season !== 0) {
    mupdate = true
  }
  if (season !== prevseason && season !== 0){
    mupdate = true
  }
  if (lang !== prevlang && season !== 0){
    mupdate = true
  }
  return mupdate
}

export const selectPlayerItem = function(PlayerList, PlayerId){
  // this is really ugly but i found no better way than breaking a list-loop
  let output
  PlayerList.some(function (item, index) {
    output = item
    return item.id == PlayerId
  });
  return output
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
