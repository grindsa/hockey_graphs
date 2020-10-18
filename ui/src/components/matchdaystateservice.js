export const changeMatchDay = function(matchdaylist, currentDay, newDay){

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
