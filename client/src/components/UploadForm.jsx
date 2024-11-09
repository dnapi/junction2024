import { useState } from 'react'
import { Typography, Button, TextField, Box } from '@mui/material'

import clashService from '../services/clashes'

const UploadForm = () => {
  const [ifsFile, setIfsFile] = useState(null)
  const [dims, setDims] = useState({
    height: 0.2,
    width: 0.1,
    length: 1.5
  })
  const [tolerance, setTolerance] = useState(0.002)
  const [distance, setDistance] = useState(0.1)

  const handleFile = (e) => {
    const ifsFile = e.target.files[0]
    setIfsFile(ifsFile)
  }

  const handleUpload = (e) => {
    e.preventDefault()

    const formData = new FormData()
    formData.append('ifc_file', ifsFile)
    console.log(formData)
    clashService.upload(formData)
  }

  const handleChangeForm = (e) => {
    const { name, value } = e.target
    setDims({
      ...dims,
      [name]: value
    })
  }

  return (
    <Box component="form" noValidate autoComplete="off">
      <Box>
        <TextField
          label="Height"
          name="height"
          value={dims.height}
          onChange={handleChangeForm}
          variant="outlined"
          type="number"
          margin="normal"
        />
        <TextField
          label="Width"
          name="width"
          value={dims.width}
          onChange={handleChangeForm}
          variant="outlined"
          type="number"
          margin="normal"
        />
        <TextField
          label="Length"
          name="length"
          value={dims.length}
          onChange={handleChangeForm}
          variant="outlined"
          type="number"
          margin="normal"
        />
      </Box>
      <Box>
        <TextField
          label="Tolerance"
          name="tolerance"
          value={tolerance}
          onChange={(e) => setTolerance(e.target.value)}
          variant="outlined"
          type="number"
          margin="normal"
        />
      </Box>
      <Box>
        <TextField
          label="Merge distance"
          name="distance"
          value={distance}
          onChange={(e) => setDistance(e.target.value)}
          variant="outlined"
          type="number"
          margin="normal"
        />
      </Box>
      <Box>
        <TextField
          type="file"
          onChange={(e) => handleFile(e)}
          variant="outlined"
          />
      </Box>
      <Box>
        <Button
          variant="contained"
          onClick={(e) => handleUpload(e)}
          // sx={{ ml: 2 }}
          >
          Upload
        </Button>
      </Box>
    </Box>
  )
}

export default UploadForm
