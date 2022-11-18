import * as React from 'react';
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import { useParams } from 'react-router-dom';
import Grid from '@mui/material/Unstable_Grid2';
import axios from 'axios';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import Config from '../utility/config';

//const Item = styled(Paper)(({ theme }) => ({
//  backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
//  ...theme.typography.body2,
//  padding: theme.spacing(1),
//  textAlign: 'center',
//  color: theme.palette.text.secondary,
//}));





const Accomodation = () => {
  const [accomodation , setAccomodation] = React.useState(null);
  const {accomodationID} = useParams();

  React.useEffect( () =>{
    const url = Config.BASE_URL+"/accomodations/"+accomodationID;
    axios.get(url)
      .then(function (response){
        setAccomodation(response.data);
      })
      .catch(function(err){
        console.log(err);
      })
  } , []);

  if(!accomodation) return null;
  
  return (
    <Grid container spacing={2}>
      <Grid xs={12}>
        <ImageList sx={{ width: 50+'%', height: 99+'%' }} cols={2} rowHeight={400}>
          {accomodation.pictures.map((item) => (
            <ImageListItem key={item}>
              <img
                //src={`${item}?w=164&h=164&fit=crop&auto=format`}
                src={`data:image/jpeg;base64,${item}`}
                //srcSet={`${item}?w=164&h=164&fit=crop&auto=format&dpr=2 2x`}
                //alt={item.title}
                //loading="lazy"
              />
            </ImageListItem>
          ))}
        </ImageList>
      </Grid>
      <Grid xs={4}>
        <h1>{accomodation.name}</h1>
      </Grid>
    </Grid>
  );
};

export default Accomodation;