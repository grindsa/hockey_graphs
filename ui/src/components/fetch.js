import axios from 'axios';
const headers = 'some headers';

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
