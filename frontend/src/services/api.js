import axios from 'axios';

const baseURL = process.env.API_URL ? `${process.env.API_URL}/api` : '/api';

const api = axios.create({
	baseURL,
	withCredentials: true,
	timeout: 15000,
});

export default api;