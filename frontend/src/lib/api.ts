import axios from "axios"

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL?.trim() || "http://localhost:8000"

export const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})
