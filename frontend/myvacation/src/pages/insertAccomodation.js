import * as React from 'react';
import Grid from '@mui/material/Unstable_Grid2';
import Button from '@mui/material/Button';
import AccomodationForm from "../components/accomodationForm";
import axios from 'axios';
import Config from'../utility/config';
import FormData from 'form-data'

async function convertFileToBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
  });
}

const InsertAccomodation = () => {
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
        const formData = new FormData();
        const images = document.getElementById("images").files;
        let convertedImages = [];
        let counter = 0;
        Array.from(images).forEach(async elem => { 
          elem = await convertFileToBase64(elem);
          convertedImages.push(elem);
          elem = dataURLtoFile(elem , "file");
          formData.append('img', elem);
        });

        console.log(formData);
        //formData.append("name" , data.get("name"));
        //formData.append("description" , data.get("description"));
        //formData.append("address" , data.get("address"));
        //formData.append("city" , data.get("city"));
        //formData.append("country" , data.get("country"));
        //formData.append("propertyType" , data.get("propertyType"));
        //formData.append("guests" , data.get("guests"));
        //formData.append("beds" , data.get("beds"));
        //formData.append("price" , data.get("price"));
        //formData.append("minimumNights" , data.get("minimumNights"));
        const result = await axios({
          method: "post",
          url: Config.BASE_URL+'/insert/accomodation' , 
          data:convertedImages,
          headers: {
            "Content-Type": "multipart/form-data"
          },
        })
        .then(function(response){
          console.log(response);
        })
        .catch(function(error){
          console.log("errore");
        });
      };

    return(
        <form onSubmit = {handleSubmit}>
        <Grid container spacing={2}>
            <AccomodationForm />
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