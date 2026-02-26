import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";
const MUSIC_URL = `${BASE_URL}/music`;
const AUTH_URL = `${BASE_URL}/auth`;

/* ===============================
   Generate Music
================================ */
export const generateMusic = async (data) => {
  const response = await axios.post(`${MUSIC_URL}/generate`, data);
  return response.data;
};

/* ===============================
   List Generated Music
================================ */
export const listMusic = async () => {
  const response = await axios.get(`${MUSIC_URL}/`);
  return response.data;
};

/* ===============================
   Download Final WAV
================================ */
export const downloadWav = (id) => {
  return `${MUSIC_URL}/download/wav/${id}`;
};

/* ===============================
   Delete Music
================================ */
export const deleteMusic = async (id) => {
  const response = await axios.delete(`${MUSIC_URL}/${id}`);
  return response.data;
};

/* ===============================
   Auth
================================ */
export const registerUser = async (data) => {
  const response = await axios.post(`${AUTH_URL}/register`, data);
  return response.data;
};

export const loginUser = async (data) => {
  const response = await axios.post(`${AUTH_URL}/login`, data);
  return response.data;
};
