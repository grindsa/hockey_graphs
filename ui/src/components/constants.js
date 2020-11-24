// constant defintion. can also be used to switch between prod and dev

const prod = {
  url: {
    API_URL: 'https://hockeygraphs.dynamop.de/api/v1/'
  }
};

const dev = {
  url: {
    API_URL: 'http://127.0.0.1:8081/api/v1/'
  }
};

export const config = process.env.NODE_ENV === 'development' ? dev : prod;

export const creatstatList = function(language){
  /* build statnames based on language setting */
  if (language == 'DE'){
    var statlist = [{id: 0, name: 'Spielstatistiken'}, {id: 1, name: 'Teamvergleich'}]
  }else{
    var statlist = [{id: 0, name: 'Match statistics'}, {id: 1, name: 'Team benchmarks'}]
  }
  return statlist
}
