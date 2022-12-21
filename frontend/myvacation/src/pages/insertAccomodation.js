import * as React from 'react';
import Grid from '@mui/material/Unstable_Grid2';
import Button from '@mui/material/Button';
import AccomodationForm from "../components/accomodationForm";
import FileInput from "../components/inputFile";
import FormData from 'form-data';
import api from '../utility/api';
import {useNavigate} from "react-router-dom";

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
        console.log("images: " , images);
        let convertedImages = [];
        let counter = 0;

        for(let i = 0 ; i < images.length; i++){
          let elem = await convertFileToBase64(images[i]);
          elem = elem.split(",")[1];
          let label = "img-"+i;
          data.append(label, elem);
        }
        data.append("imagesLength" , images.length);
        console.log("form: " , data);
        const headers = {'Content-type': 'multipart/form-data'};
        const result = await api.post('/insert/accomodation' , 
          data,
          //{headers: headers}
        )
        .then(function(response){
          console.log(response.data);
          navigate("/accomodation/"+response.data.accomodationID);
        })
        .catch(function(error){
          console.log("errore");
        });
      };

    return(
        <form onSubmit = {handleSubmit}>
        <Grid container spacing={2}>
            <AccomodationForm />
            {/*<FileInput label="Immagini"></FileInput>*/}
            <Grid xs = {3} />
            <Grid xs = {6}>
                <Button
                  type="submit"
                  fullWidth
                  variant="contained"
                  sx={{ mt: 3, mb: 2 }}
                >
                  Modifica
                </Button>
            </Grid>
        </Grid>
        </form>
    );
};

export default InsertAccomodation;