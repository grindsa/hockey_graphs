// constant defintion. can also be used to switch between prod and dev

const prod = {
  url: {
    API_URL: 'https://hockeygraphs.dynamop.de/api/v1/'
  }
};

const dev = {
  url: {
    API_URL: 'http://127.0.0.1:8081/api/v1/'
    // API_URL: 'http://192.168.123.21:8081/api/v1/'
  }
};

// export const config = process.env.NODE_ENV === 'development' ? dev : prod;
export const config = process.env.NODE_ENV === 'development' ? prod : prod;
