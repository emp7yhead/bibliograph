import jwtDecode from 'jwt-decode';
import moment from 'moment/moment';
import axios from 'axios';
import config from '../config';

const localStorageTokenInterceptor = (config) => {
  const headers = {};
  const rawToken = localStorage.getItem('token');

  if (rawToken) {
    const token = JSON.parse(rawToken);
    const decodedAccessToken = jwtDecode(token.access_token);
    const isAccessTokenValid = moment.unix(decodedAccessToken.exp).toDate() > new Date();

    if (isAccessTokenValid) {
      headers.Authorizartion = `Bearer ${token.access_token}`;
    } else {
      alert('Login session is expired');
    }
  }

  config.headers = headers;
  return config;
};

class BibliographClient {
  constructor(overrides) {
    this.config = {
      ...config,
      ...overrides,
    };

    this.apiClient = this.getApiClient(config);
  }

  getApiClient(config) {
    const initialConfig = {
      baseURL: `http://localhost:5000/api/v1`,
    };
    const client = axios.create(initialConfig);
    client.interceptors.request.use(localStorageTokenInterceptor);
    return client;
  }

  register(username, email, password) {
    const loginData = {
      username,
      email,
      password,
    };

    return this.apiClient.post('register', loginData).then(
      (resp) => resp.data,
    );
  }
}

export default BibliographClient;
