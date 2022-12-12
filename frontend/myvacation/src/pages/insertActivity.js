import * as React from 'react';
import Grid from '@mui/material/Unstable_Grid2';
import Button from '@mui/material/Button';
import ActivityForm from "../components/activityForm";
import FileInput from "../components/inputFile";
import FormData from 'form-data';
import api from '../api/api';
import {useNavigate} from "react-router-dom";
import { convertFileToBase64 } from '../utility/utility';

const InsertActivity = () => {
  let navigate = useNavigate();

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
        const result = await api.post('/insert/activity' , 
          data,
          //{headers: headers}
        )
        .then(function(response){
          console.log(response.data);
          navigate("/activity/"+response.data.activityID);
        })
        .catch(function(error){
          console.log("errore");
        });
    };

    return(
        <form onSubmit = {handleSubmit}>
        <ActivityForm />
        <Grid container spacing={2}>
            {/*<FileInput label="Immagini"></FileInput>*/}
            <Grid xs = {3}/>
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

export default InsertActivity;