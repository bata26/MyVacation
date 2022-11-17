import * as React from 'react';
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import { useParams } from 'react-router-dom';
import Grid from '@mui/material/Unstable_Grid2';
import axios from 'axios';
import Config from '../utility/config';

const Item = styled(Paper)(({ theme }) => ({
  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
  ...theme.typography.body2,
  padding: theme.spacing(1),
  textAlign: 'center',
  color: theme.palette.text.secondary,
}));


function getAccomodationByID(accomodationID){

  const url = Config.BASE_URL+"/accomodations/"+accomodationID;
  console.log(url);
  axios.get(url ,{ 
    //headers: {
    //  "Access-Control-Allow-Origin": '*'
    //}
  })
  .then(function (response){
    console.log(response);
  })
  .catch(function(err){
    console.log(err);
  })
}


const Accomodation = () => {
    
    const {accomodationID} = useParams();
    const response = getAccomodationByID(accomodationID);
    return (
      <Grid container spacing={2}>
      <Grid xs={12}>
        <Item>{accomodationID}</Item>
      </Grid>
      <Grid xs={4}>
        <Item>xs=4</Item>
      </Grid>
      <Grid xs={4}>
        <Item>xs=4</Item>
      </Grid>
      <Grid xs={8}>
        <Item>xs=8</Item>
      </Grid>
    </Grid>
  );
};

export default Accomodation;