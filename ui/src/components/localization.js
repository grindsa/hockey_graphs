export const creatstatList = function(language){
  /* build statnames based on language setting */
  if (language == 'DE'){
    var statlist = [{id: 0, name: 'Spielstatistiken'}, {id: 1, name: 'Teamvergleich'}]
  }else{
    var statlist = [{id: 0, name: 'Match statistics'}, {id: 1, name: 'Team benchmarks'}]
  }
  return statlist
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


export const createTcSliderText = function(language, select, max){
  if (language == 'DE'){
    if (select === max) {
      var slidermessage = 'Gesamte Saison'
    }else if (max - select === 1) {
      var slidermessage = 'letztes Spiel'
    }else{
      var slidermessage = 'letzte ' + (max-select) + ' Spiele'
    }
  }else{
    if (select === max) {
      var slidermessage = 'Full Season'
    }else if (max - select === 1) {
      var slidermessage = 'last match'
    }else{
      var slidermessage = 'last '+ (max-select) + ' matches'
    }
  }

  return slidermessage
}