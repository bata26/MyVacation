import * as React from 'react';
import Button from '@mui/material/Button';
import AccomodationForm from "../components/accomodationForm";
import FormData from 'form-data';
import api from '../utility/api';
import { useNavigate } from "react-router-dom";
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

async function convertFileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
  });
}

const InsertAccomodation = () => {
  let navigate = useNavigate();
  const dataURLtoFile = (dataurl, filename) => {
    const arr = dataurl.split(',')
    const mime = arr[0].match(/:(.*?);/)[1]
    const bstr = atob(arr[1])
    let n = bstr.length
    const u8arr = new Uint8Array(n)
    while (n) {
      u8arr[n - 1] = bstr.charCodeAt(n - 1)
      n -= 1 // to make eslint happy
    }
    return new File([u8arr], filename, { type: mime })
  }

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    //const formData = new FormData();
    const images = document.getElementById("images").files;
    let convertedImages = [];
    let counter = 0;

    for (let i = 0; i < images.length; i++) {
      let elem = await convertFileToBase64(images[i]);
      elem = elem.split(",")[1];
      let label = "img-" + i;
      data.append(label, elem);
    }
    data.append("imagesLength", images.length);
    const headers = { 'Content-type': 'multipart/form-data' };
    const result = await api.post('/insert/accomodation', data)
      .then(function (response) {
        navigate("/accomodation/" + response.data.accomodationID);
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
  };

  return (
    <form onSubmit={handleSubmit}>
      <Container component="main" maxWidth="lg">
        <CssBaseline />
        <Box
          sx={{
            pt: 8,
            pb: 6,
          }}
        >
          <Container maxWidth="lg">
            <Typography
              component="h1"
              variant="h2"
              align="center"
              color="text.primary"
              gutterBottom
            >
              Insert accomodation
            </Typography>
          </Container>
        </Box>
        <AccomodationForm />
        <Container maxWidth='md'>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 2 }}
          >
            Insert
          </Button>
        </Container>
      </Container>
      <Box
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
        }}
      >
      </Box>
    </form>
  );
};

export default InsertAccomodation;