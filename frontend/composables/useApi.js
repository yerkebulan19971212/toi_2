import axios from 'axios'

export const useApi = () => {
  const config = useRuntimeConfig()
  const baseURL = config.public.apiBase

  const client = axios.create({
    baseURL,
    headers: { 'Content-Type': 'application/json' },
  })

  const get = (endpoint, params = {}) =>
    client.get(endpoint, { params }).then((r) => r.data)

  const post = (endpoint, data) =>
    client.post(endpoint, data).then((r) => r.data)

  const postForm = (endpoint, formData) =>
    client
      .post(endpoint, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
      .then((r) => r.data)

  return { get, post, postForm, baseURL }
}
