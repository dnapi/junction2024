import axios from 'axios'

const baseUrl = '/api/upload'

const upload = (formData) => {
  const config = {
    headers: {
      accept: 'application/json',
      'Content-Type': 'multipart/form-data'
    }
  }

  console.log(formData)
  const request = axios.post(baseUrl, formData, config)
  console.log(request)
  return request.then((response) => response.data)
}

export default { upload }
