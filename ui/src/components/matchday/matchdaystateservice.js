export const changeMatchDay = function(matchdaylist, currentDay, newDay){
  /* change "displayday" key in data structure to show another matchday */
  for (var key in matchdaylist) {
    if (!matchdaylist.hasOwnProperty(key)) {
        continue;
    }
    if(key === currentDay){
      // console.log('curr', key, matchdaylist[key]['displayday']);
      matchdaylist[key]['displayday'] = false
    }else if(key === newDay){
      // console.log('new', key, matchdaylist[key]['displayday']);
      matchdaylist[key]['displayday'] = true
    }
  }
  return matchdaylist
}

export const checkMatchdayUpdate = function(matchdays, prevmatchdays, season, prevseason){
  /* this is to check if we have to fetch matchdays list from rest */
  // console.log(matchdays, prevmatchdays, season, prevseason)
  var mupdate = false
  if (matchdays !== prevmatchdays && season !== 0) {
    mupdate = true
  }
  if (season !== prevseason && season !== 0){
    mupdate = true
  }
  return mupdate
}
