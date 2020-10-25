/* functions to be shared between different components */
import { GET } from './fetch.js';

export const isEmpty = function(obj){
  /* check if object is empty */
  for(var key in obj) {
      if(obj.hasOwnProperty(key))
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
