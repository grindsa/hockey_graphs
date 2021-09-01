export const creatstatList = function(language){
  /* build statnames based on language setting */
  var statlist = [{id: 0, name: 'Match statistics', route: '/matchstatistics'}, {id: 1, name: 'Team benchmarks', route: '/teamcomparison'}, {id: 2, name: 'Player statistics', route: '/playerstatistics'}]
  if (language == 'DE'){
    statlist = [{id: 0, name: 'Spielstatistiken', route: '/matchstatistics'}, {id: 1, name: 'Teamvergleich', route: '/teamcomparison'}, {id: 2, name: 'Spielerstatistiken', route: '/playerstatistics'}]
  }
  return statlist
}

export const createnostatMessage = function(language){
  /* build no message based on language setting */
  var nostatmessage = 'No statistics available.'
  if (language == 'DE'){
    nostatmessage = 'Keine Statistiken verfügbar'
  }
  return nostatmessage
}

export const createnoChartMessage = function(language){
  /* build no message based on language setting */
  var nostatmessage = 'No data to render chart.'
  if (language == 'DE'){
    nostatmessage = 'Keine Daten verfügbar.'
  }
  return nostatmessage
}

export const createTcSliderText = function(language, select, max){
  let slidermessage
  if (language == 'DE'){
    if (select === max) {
      slidermessage = 'Gesamte Saison'
    /* }else if (max - select === 1) {
      var slidermessage = 'letztes Spiel' */
    }else{
      slidermessage = select + '. Spieletag'
    }
  }else{
    if (select === max) {
      slidermessage = 'Full Season'
    }else if (select === 1) {
      slidermessage = '1st Matchday'
    }else if (select === 2) {
      slidermessage = '2nd Matchday'
    }else if (select === 3) {
      slidermessage = '3rd Matchday'
    }else{
      slidermessage = select + 'th Matchday'
    }
  }
  return slidermessage
}
