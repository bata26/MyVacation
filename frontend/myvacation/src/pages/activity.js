import * as React from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import Config from '../utility/config';
import ReactHtmlParser from 'react-html-parser';
import api from "../utility/api";
import ReviewForm from '../components/reviewForm';
import Button from '@mui/material/Button';
import { Typography } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import DateRangePicker from "../components/datePicker";
import { useNavigate } from "react-router-dom";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';


const theme = createTheme();

const Activity = () => {
  const [activity , setActivity] = React.useState(null);
  const [reviews, setReviews] = React.useState(null);
  const [enableButton, setEnableButton] = React.useState(null);
  const [searchParams] = useSearchParams();
  const { activityID } = useParams();
  const [startDate, setStartDate] = React.useState(searchParams.get("startDate") === "" ? null : searchParams.get("startDate"))
  const [guests, setGuests] = React.useState(searchParams.get("guests") === "" ? null : searchParams.get("guests"))

  const navigate = useNavigate();


  React.useEffect( () =>{
        api.get("/activities/"+activityID)
            .then(function (response){
                setActivity(response.data);
                setReviews(response.data.reviews)
                console.log(response.data)
                console.log(response.data.reviews.length)
                console.log(parseInt(process.env.REACT_APP_REVIEWS_SIZE))
                if(response.data.reviews.length >= parseInt(process.env.REACT_APP_REVIEWS_SIZE))
                    setEnableButton(true)
                else
                    setEnableButton(false)
            })
            .catch(function(err){
                console.log(err);
            })
  } , []);

  //Metodo per eliminare activity
  const deleteActivity = (activityID) => {
    api.delete("/activities/" + activityID)
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
    navigate('/search')
  }

  function goToCheckout(){
        navigate("/checkout?startDate=" + startDate + "&type=activities" + "&id=" + activity._id + "&guests=" + guests)
  }

  const getAllReviews = async () => {
        await api.get("/reviewsByDestination/" + activityID)
            .then(function (response) {
                setReviews(response.data)
                setEnableButton(false)
                console.log(response.data)
            })
            .catch(function (error) {
                console.log(error);
            });
  }

  if(!activity) return null;
  
  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xl">
        <CssBaseline />
        <Box>
          <Box
            sx={{
              pt: 8,
              pb: 6,
            }}
          >
            <Container maxWidth="xl">
              <Typography
                component="h1"
                variant="h2"
                align="center"
                color="text.primary"
                gutterBottom
              >
                {activity.name}
              </Typography>
            </Container>
          </Box>
        </Box>
      </Container>

      {/* Immagine */}
      <Container maxWidth='lg'>
        <img
          src={`data:image/jpeg;base64,${activity.mainPicture}`}
          style={{ borderRadius: 10 + 'px', height: 100 + '%', width: 99 + '%', marginTop: 3 + 'px' }}
        />
      </Container>

      <Container maxWidth='lg'>
        <Typography
          component="h2"
          variant="h4"
          align="left"
          color="text.primary"
          gutterBottom
          sx={{ mt: 2 }}
        >
          Description
        </Typography>

        <Typography
          component="h2"
          variant="h6"
          align="left"
          color="text.primary"
        >
          {ReactHtmlParser(activity.description)}
        </Typography>


        <Typography
          component="h3"
          variant="h4"
          align="right"
          color="text.primary"
          gutterBottom
        >
          Price
        </Typography>

        <Typography
          align='right'
          component="h3"
          variant="h5"
          color="text.primary"
          sx={{ mb: 2 }}
        >
          {activity.price}€
        </Typography>

        <Typography
          component="h3"
          variant="h4"
          align="right"
          color="text.primary"
          gutterBottom
        >
          Other information
        </Typography>

            <Typography align='right' sx={{mb: 2}}>
              Host: {activity.host_name}
              <br/>
              Duration: {activity.duration}H
              <br/>
              Address: {activity.location.address}
              <br/>
              Country: {activity.location.country}
              <br/>
              City: {activity.location.city}
            </Typography>


        <Box sx={{ ml: 35, mb: 2 }}>
          <DateRangePicker startDate={startDate} />
        </Box>

        {startDate != null && localStorage.getItem("userID") != null && guests != null ?
          <Button
            fullWidth
            variant="contained"
            sx={{ mb: 2 }}
            onClick={() => goToCheckout()}>
            Book activity
          </Button> : <></>}

        <ReviewForm destinationID={activity._id} destinationType={"activity"} />

        {
          localStorage.getItem("userID") === activity.host_id || localStorage.getItem("role") === "admin" ?
            (
              <Button
                fullWidth
                variant="contained"
                color='error'
                sx={{ mt: 2 }}
                onClick={() => { deleteActivity(activity._id) }}
              >
                Delete Activity
              </Button>
            )
            : <></>
        }
      </Container>
      <Box
      sx={{
          py: 3,
          px: 2,
          mt: 'auto',
      }}
      >
      </Box>

      <Container maxWidth='lg'>
        <Typography
          component="h2"
          variant="h4"
          align="center"
          color="text.primary"
          gutterBottom
          sx={{ mt: 2 }}
        >
          Reviews
        </Typography>
        <Grid
        sx={{ overflowY: "scroll", maxHeight: "1160px" }}
        >
        {reviews && reviews.map((item) => (
        <Card key={item._id} sx={{ maxHeight: 100 , marginTop: 2}}>
          <CardContent>
            <Typography gutterBottom variant="h5" component="div">
              {item.reviewer} - {item.score}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {item.description}
            </Typography>
          </CardContent>
        </Card>
        ))}
        </Grid>
        {enableButton ?
            <Container maxWidth='sm'>
                <Button
                fullWidth
                variant="contained"
                sx={{ mt: 2 }}
                onClick={() => {getAllReviews()}}
                >
                More reviews
                </Button>
            </Container> : <></>}
      </Container>
      
      <Box
      component="footer"
      sx={{
          py: 3,
          px: 2,
          mt: 'auto',
      }}
      >
      </Box>
    </ThemeProvider>

  );
};

export default Activity;