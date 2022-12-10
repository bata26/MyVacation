import * as React from 'react';
import { styled } from '@mui/material/styles';
import Paper from '@mui/material/Paper';
import { useParams , useSearchParams } from 'react-router-dom';
import Grid from '@mui/material/Unstable_Grid2';
import axios from 'axios';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import Config from '../utility/config';
import ReactHtmlParser from 'react-html-parser';
import { borderRadius } from '@mui/system';
import ReactRoundedImage from "react-rounded-image";
import Separator from "../components/separator";
import DateRangePicker from "../components/datePicker";
import api from "../api/api";
import Button from '@mui/material/Button';
import ReviewForm from '../components/reviewForm';

function srcset(image, size, rows = 1, cols = 1) {
  return {
    src: `${image}?w=${size * cols}&h=${size * rows}&fit=crop&auto=format`,
    srcSet: `${image}?w=${size * cols}&h=${
      size * rows
    }&fit=crop&auto=format&dpr=2 2x`,
  };
}

function bookAccomodation(accomodation , startDate , endDate){
  console.log(accomodation);
  console.log(startDate);
  console.log(endDate);

  if(startDate === null || endDate === null){
    alert("Torna indietro e inserisci le date per effettuare la prenotazione!");
    return;
  }
  const bodyRequest = {
    "accomodation" : accomodation,
    "startDate" : startDate,
    "endDate" : endDate,
  };
  api.post("/book/accomodation" , bodyRequest)
  .then(function(response){
    alert("prenotazione avvenuta con successo");
  })
  .catch(function(error){
    console.log("error : " , error);
    alert("Impossibile prenotare, riprova più tardi");
  })
}

const Accomodation = () => {
  const [accomodation , setAccomodation] = React.useState(null);
  const [searchParams] = useSearchParams();
  const {accomodationID} = useParams();
  const startDate = searchParams.get("startDate");
  const endDate = searchParams.get("endDate");

  React.useEffect( () =>{
    const url = Config.BASE_URL+"/accomodations/"+accomodationID;
    api.get("/accomodations/"+accomodationID)
    .then(function(response){
      setAccomodation(response.data);
    })
    .catch(function(error){
      console.log(error);
    });

    //axios.get(url)
    //  .then(function (response){
    //    setAccomodation(response.data);
    //  })
    //  .catch(function(err){
    //    console.log(err);
    //  })
  } , []);

  if(!accomodation) return null;
  
  return (
    <Grid container spacing={2}>
      <Grid xs={2}/>
      <Grid xs={8}>
        {/*<ImageList sx={{ width: 50+'%', height: 99+'%' }} cols={2} rowHeight={400}> */}
          <ImageList
        sx={{ width: 100+'%', height: 99+'%'}}
        variant="quilted"
        gap={5}
        cols={3}
        rowHeight={200}
      >
        <ImageListItem key={accomodation.mainPicture} cols={2} rows={3}>
            <img
              src={`data:image/jpeg;base64,${accomodation.mainPicture}`}
              style={{borderRadius:10 + 'px'}}
            />
        </ImageListItem>
          {accomodation.pictures.map((item) => (
            <ImageListItem key={item}>
              <img
                src={`data:image/jpeg;base64,${item}`}
                style={{borderRadius:10 + 'px'}}
              />
          </ImageListItem>
          ))}
        </ImageList>
      </Grid>
      <Grid xs={2}/>
      {/** ROW 1 */}
      <Grid xs={2}/>
      <Grid xs={4}>
        <h1>{accomodation.name}</h1>
      </Grid>
      <Grid xs={1}/>
      <Grid xs={3}>
        <h2>Host: <i>{accomodation.host_name}</i></h2>
      </Grid>
      <Grid xs={2}/>

      {/** ROW 2 */}
      <Grid xs={2}/>
      <Grid xs={4}>
        <span><strong>{accomodation.property_type}</strong></span>
        <br></br>
        <br></br>
        <span>{ReactHtmlParser(accomodation.description)}</span>
      </Grid>
      
      <Grid xs={4} style={{borderRadius:10+'px', boxShadow:'1px 2px 9px #8a8987'}}>
        {/*<ReactRoundedImage
          image={`data:image/jpeg;base64,${accomodation.host_picture}`}
          roundedColor="#fff"
          imageWidth="150"
          imageHeight="150"
          roundedSize="8"
          borderRadius="50"
          hoverColor="#DD1144"
          style={{Cursor:'pointer'}}
          />*/}
        <DateRangePicker startDate={startDate} endDate={endDate}/>
      </Grid>
      <Grid xs={1}/>

      {/** ROW 3 */}
      <Grid xs={2}/>
      <Grid xs={4}>
        <Separator />
      </Grid>
      <Grid xs={4}>
        <Separator />
      </Grid>
      <Grid xs={2}/>

      {/** ROW 4 */}
      <Grid xs={2}/>
      <Grid xs={4}>
            <h3>Informazioni</h3>
      </Grid>
      <Grid xs={4}>
        <Button variant="contained" style={{width:100+'%'}} onClick={()=> bookAccomodation(accomodation , startDate , endDate)}>Prenota</Button>
      </Grid>
      <Grid xs={2}/>

      {/** ROW 5 */}
      <Grid xs={2}/>
      <Grid xs={2}>
        <span>{accomodation.accommodates} <strong>ospiti</strong></span>
      </Grid>
      <Grid xs={2}>
        <span>{accomodation.bedrooms} <strong>camere da letto</strong></span>
      </Grid>
      <Grid xs={4}>
        <ReviewForm destinationID={accomodation._id}/>
      </Grid>
      <Grid xs={2}/>

      {/** ROW 5 */}
      <Grid xs={2}/>
      <Grid xs={2}>
        <span>{accomodation.beds} <strong>Letti</strong></span>
      </Grid>
      <Grid xs={2}>
        <span><strong>Minimo </strong>{accomodation.minimum_nights} <strong>notti</strong></span>
      </Grid>
      <Grid xs={6}/>

      {/** ROW 8 */}
      <Grid xs={2}/>
      <Grid xs={4}>
        <Separator />
      </Grid>
      <Grid xs={6}/>


      {/** ROW 4 */}
      <Grid xs={2}/>
      <Grid xs={4}>
            <h3>Posizione</h3>
      </Grid>
      <Grid xs={6}/>

      {/** ROW 5 */}
      <Grid xs={2}/>
      <Grid xs={4}>
            <span><strong>Indirizzo:</strong></span>
            <span>{accomodation.location.address}</span>
      </Grid>
      <Grid xs={6}/>

      {/** ROW 6 */}
      <Grid xs={2}/>
      <Grid xs={4}>
            <span><strong>Città: </strong></span>
            <span>{accomodation.location.city}</span>
      </Grid>
      <Grid xs={6}/>

      {/** ROW 7 */}
      <Grid xs={2}/>
      <Grid xs={4}>
            <span><strong>Nazione:</strong></span>
            <span>{accomodation.location.country}</span>
      </Grid>
      <Grid xs={6}/>

      {/** ROW 8 */}
      <Grid xs={2}/>
      <Grid xs={4}>
        <Separator />
      </Grid>
      <Grid xs={6}/>
          
    </Grid>
  );
};

export default Accomodation;