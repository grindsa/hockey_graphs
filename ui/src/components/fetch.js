import axios from 'axios';
const headers = 'some headers';

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

export const GET = url => {
    return axios.get(url);
}

export const POST = (url, data) => {
    return axios(url, {
        method: 'POST',
        headers,
        data,
    });
}
