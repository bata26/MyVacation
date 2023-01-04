import * as React from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import ReactHtmlParser from 'react-html-parser';
import api from "../utility/api";
import ReviewForm from '../components/reviewForm';
import Button from '@mui/material/Button';
import { CardActions, Typography } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import { useNavigate } from "react-router-dom";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Grid from '@mui/material/Grid';
import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';
import ThumbUpOffAltIcon from '@mui/icons-material/ThumbUpOffAlt';



const theme = createTheme();

const Activity = () => {
  const [activity, setActivity] = React.useState(null);
  const [reviews, setReviews] = React.useState(null);
  const [totLikes, setTotLikes] = React.useState(null);
  const [enableButton, setEnableButton] = React.useState(null);
  const [likedAdv, setLikedAdv] = React.useState(null);
  const [searchParams] = useSearchParams();
  const { activityID } = useParams();
  const [startDate, setStartDate] = React.useState(searchParams.get("startDate") === "" ? null : searchParams.get("startDate"))
  const [guests, setGuests] = React.useState(searchParams.get("guests") === "" ? null : searchParams.get("guests"))

  const navigate = useNavigate();

  function getTotalLikes() {
    api.get('/likenumber/activity/' + activityID)
      .then(function (response) {
        setTotLikes(response.data.likes)
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
  }
  React.useEffect(() => {
    api.get("/activities/" + activityID)
      .then(function (response) {
        setActivity(response.data);
        setReviews(response.data.reviews)
        if (response.data.reviews.length >= parseInt(process.env.REACT_APP_REVIEWS_SIZE))
          setEnableButton(true)
        else
          setEnableButton(false)
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      })

    api.get("/users/liking/activity/" + activityID)
      .then(function (response) {

        setLikedAdv(response.data.liked)

      })
      .catch(function (error) {
        console.log(error);
      });
    getTotalLikes();


  }, []);


  //Metodo per eliminare review
  const deleteReview = async (reviewID) => {
    await api.delete("/reviews/activity/" + activityID + "/" + reviewID)
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
    window.location.reload(false);
  }

  //Metodo per eliminare activity
  const deleteActivity = (activityID) => {
    api.delete("/activities/" + activityID)
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
    navigate('/search')
  }

  const likeAdv = async (likedAdvID, likedAdvName) => {
    await api.post("/users/liking", {
      "likedAdvID": likedAdvID,
      "likedAdvName": likedAdvName,
      "destinationType": "activity"
    }).then(function (response) {
      console.log(response.data);
      setLikedAdv(true);
      getTotalLikes();
    }).catch(function (error) {
      console.log(error);
    });
  }

  const unlikeAdv = async (unlikedAdvID, unlikedAdvName) => {
    await api.post("/users/unliking", {
      "unlikedAdvID": unlikedAdvID,
      "unlikedAdvName": unlikedAdvName,
      "destinationType": "activity"
    }).then(function (response) {
      console.log(response.data);
      setLikedAdv(false);
      getTotalLikes();
    }).catch(function (error) {
      console.log(error);
    });
  }

  function goToCheckout() {
    navigate("/checkout?startDate=" + startDate + "&type=activities" + "&id=" + activity._id + "&guests=" + guests)
  }

  const getAllReviews = async () => {
    await api.get("/reviewsByDestination/" + activityID)
      .then(function (response) {
        setReviews(response.data)
        setEnableButton(false)
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
  }

  if (!activity) return null;

  return (
    ((activity && activity.approved) || (activity && !activity.approved && localStorage.getItem("userID") === activity.hostID) || localStorage.getItem("role") === "admin") ?
      (<ThemeProvider theme={theme}>
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
          <Grid alignItems={"left"}>
            {localStorage.getItem("userID") != null && activity.approved && localStorage.getItem("role") !== "admin" ?
              (!likedAdv ?
                <Button onClick={() => { likeAdv(activity._id, activity.name) }}>
                  <ThumbUpOffAltIcon
                    variant="filled"
                    sx={{ fontSize: 40 }}
                  />
                </Button>
                :
                <Button onClick={() => { unlikeAdv(activity._id, activity.name) }}>
                  <ThumbUpAltIcon
                    variant="filled"
                    sx={{ fontSize: 40 }}
                  />
                </Button>
              ) : <></>
            }
            <Typography>
              <b>{totLikes}</b>
            </Typography>
          </Grid>
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

          <Typography align='right' sx={{ mb: 2 }}>
            <b>Host:</b> {activity.hostName}
            <br />
            <b>Duration:</b> {activity.duration}H
            <br />
            <b>Address:</b> {activity.location.address}
            <br />
            <b>Country:</b> {activity.location.country}
            <br />
            <b>City:</b> {activity.location.city}
            <br />
            {startDate ?
              <>
                <b>Start date:</b> {startDate}
              </> : <></>
            }
          </Typography>
          {startDate != null && localStorage.getItem("userID") != null && guests != null && activity.approved && localStorage.getItem("role") !== "admin" ?
            <Button
              fullWidth
              variant="contained"
              color="success"
              sx={{ mb: 2 }}
              onClick={() => goToCheckout()}>
              Book activity
            </Button> : <></>}
          {(localStorage.getItem("userID") === activity.hostID || localStorage.getItem("role") === "admin") && activity.approved ?
            (<>
              <Button
                fullWidth
                variant="contained"
                color='error'
                sx={{ mt: 2 }}
                onClick={() => { deleteActivity(activity._id) }}
              >
                Delete Activity
              </Button>
              <Button
                fullWidth
                variant="contained"
                color='info'
                sx={{ mt: 2 }}
                onClick={() => { navigate("/update/activity/" + activityID) }}
              >
                Update Activity
              </Button>
            </>) : <></>
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
        {activity.approved ?
          (<>
            <ReviewForm destinationID={activity._id} destinationType={"activity"} />
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
                sx={{ overflowY: "scroll", maxHeight: "1460px" }}
              >
                {reviews && reviews.map((item) => (
                  <Card key={item._id} sx={{ maxHeight: 180, marginTop: 2 }}>
                    <CardContent>
                      <Typography gutterBottom variant="h5" component="div">
                        {item.reviewer} - {item.score}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {item.description}
                      </Typography>
                    </CardContent>
                    <CardActions>
                      {localStorage.getItem("userID") && (localStorage.getItem("userID") === item.userID || localStorage.getItem("role") === "admin") ?
                        <Button color='error' onClick={() => { deleteReview(item._id) }}>
                          Delete
                        </Button> : <></>
                      }
                      {localStorage.getItem("userID") ?
                        <Button color='info' onClick={() => navigate("/profile/" + item.userID)}>
                          View Profile
                        </Button> : <></>
                      }
                    </CardActions>
                  </Card>
                ))}
              </Grid>
              {enableButton ?
                <Container maxWidth='sm'>
                  <Button
                    fullWidth
                    variant="contained"
                    sx={{ mt: 2 }}
                    onClick={() => { getAllReviews() }}
                  >
                    More reviews
                  </Button>
                </Container> : <></>}
            </Container>
          </>) : <></>}
        <Box
          sx={{
            py: 3,
            px: 2,
            mt: 'auto',
          }}
        >
        </Box>
      </ThemeProvider>) : <></>
  );
};

export default Activity;