import { useStore } from '@/store/store';
import { CustomError } from '@/types/custom-error.type';
import axios from 'axios';

const baseURL = import.meta.env.VITE_API_BASE_URL;

const options = {
  baseURL,
  withCredentials: true,
  timeout: 10000,
};

const API = axios.create(options);

API.interceptors.request.use(
  (config) => {
    const accessToken = useStore.getState().accessToken;
    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

API.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    const data = error.response?.data;

    const customError: CustomError = {
      ...error,
      message:
        data?.message ||
        (error.response
          ? 'The request could not be completed.'
          : 'Cannot connect to the server. Make sure the backend is running and try again.'),
      errorCode: data?.errorCode || (error.response ? 'UNKNOWN_ERROR' : 'NETWORK_ERROR'),
    };

    return Promise.reject(customError);
  }
);

export default API;

