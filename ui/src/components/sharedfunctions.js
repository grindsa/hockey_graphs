/* functions to be shared between different components */
import { GET } from './fetch.js';
import Cookies from 'universal-cookie';

export const isEmpty = function(obj){
  /* check if object is empty */
  for(var key in obj) {
      if (Object.prototype.hasOwnProperty.call(obj, key))
      // if(obj.hasOwnProperty(key))
          return false;
  }
  return true;
}

export async function asyncGET(apiEndpoint){
  if(apiEndpoint){
    const { data: Items } = await GET(apiEndpoint);
    if (Items) {
      return Items
    }else{
      // error
    }
  }
}

export function CookieSet(app_name, options){
    // save state to coookie
    const cookies = new Cookies();
    cookies.set(app_name, {language: options.language, selectedSeason: options.selectedSeason, selectedStat: options.selectedStat, foo: 'WannaSeeUrFaceOnceUreadThis'}, { path: '/', maxAge: 2419200 });
}

export function getParams(location) {
  const searchParams = new URLSearchParams(location.search);
  return {
    lang: searchParams.get('lang') || '',
  };
}
