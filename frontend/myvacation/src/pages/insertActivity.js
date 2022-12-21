import * as React from 'react';
import Grid from '@mui/material/Unstable_Grid2';
import Button from '@mui/material/Button';
import ActivityForm from "../components/activityForm";
import FileInput from "../components/inputFile";
import FormData from 'form-data';
import api from '../utility/api';
import { useNavigate } from "react-router-dom";
import { convertFileToBase64 } from '../utility/utility';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const InsertActivity = () => {
  let navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    //const formData = new FormData();
    const images = document.getElementById("images").files;
    console.log("images: ", images);
    let convertedImages = [];
    let counter = 0;

    for (let i = 0; i < images.length; i++) {
      let elem = await convertFileToBase64(images[i]);
      elem = elem.split(",")[1];
      let label = "img-" + i;
      data.append(label, elem);
    }
    data.append("imagesLength", images.length);
    console.log("form: ", data);
    const headers = { 'Content-type': 'multipart/form-data' };
    const result = await api.post('/insert/activity',
      data,
      //{headers: headers}
    )
      .then(function (response) {
        console.log(response.data);
        navigate("/activity/" + response.data.activityID);
      })
      .catch(function (error) {
        console.log("errore");
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
              Insert activity
            </Typography>
          </Container>
        </Box>
        <ActivityForm />
        <Container maxWidth='md'>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 2 }}
            onClick={{ handleSubmit }}
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

export default InsertActivity;