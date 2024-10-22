import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import api from "../utility/api";
import Moment from 'moment';
import DeleteIcon from '@mui/icons-material/Delete';
import EditReservationModal from "../components/editReservationModal";
import EditProfileModal from "../components/editProfileModal";
import { useNavigate, useParams } from 'react-router-dom';
import Button from '@mui/material/Button';
import Link from '@mui/material/Link';

const theme = createTheme();

const Profile = () => {
  const [profile, setProfile] = React.useState(null);
  const [reservations, setReservations] = React.useState([]);
  const [listFollowedUsers, setListFollowedUsers] = React.useState([]);
  const [listLikedAcc, setListLikedAcc] = React.useState([]);
  const [listLikedAct, setListLikedAct] = React.useState([]);
  const [listCommonLikedAcc, setListCommonLikedAcc] = React.useState([]);
  const [listCommonLikedAct, setListCommonLikedAct] = React.useState([]);
  const [isFollowing, setIsFollowing] = React.useState(null);
  const navigate = useNavigate();
  const { profileID } = useParams();


  React.useEffect(() => {

    //Richiesta per recuperare le informazioni dell'utente
    api.get("/users/" + profileID)
      .then(function (response) {
        setProfile(response.data);
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });

    //Richiesta per recuperare le persone seguite dall'utente
    api.get("/users/following/" + profileID)
      .then(function (response) {
        setListFollowedUsers(response.data);
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });


    //Richiesta per recuperare le persone seguite dall'utente
    api.get("/users/isfollowing/" + profileID)
      .then(function (response) {
        setIsFollowing(response.data.following);
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });

    //Richiesta per recuperare gli alloggi piaciuti all'utente
    api.get("/users/liked/accommodation/" + profileID)
      .then(function (response) {
        setListLikedAcc(response.data)
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });

    //Richiesta per recuperare le attività piaciute all'utente
    api.get("/users/liked/activity/" + profileID)
      .then(function (response) {
        setListLikedAct(response.data)
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });

    if (profileID !== localStorage.getItem("userID")) {
      //Richiesta per recuperare gli alloggi piaciuti all'utente in comune
      api.get("/commonadvs/accommodation/" + profileID)
        .then(function (response) {
          setListCommonLikedAcc(response.data)
        })
        .catch(function (error) {
          alert("Ops, something went wrong :(" + "\n" + error);
        });

      //Richiesta per recuperare le attività piaciute all'utente in comune
      api.get("/commonadvs/activity/" + profileID)
        .then(function (response) {
          setListCommonLikedAct(response.data)
        })
        .catch(function (error) {
          alert("Ops, something went wrong :(" + "\n" + error);
        });
    }
  }, []);

  if (!profile) return null;

  //Metodo per eliminare reservation
  const deleteReservation = async (reservationID) => {
    await api.delete("/reservations/" + reservationID)
      .then(function (response) {
        window.location.reload(true);
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
  }

  const deleteProfile = async (profileID) => {
    await api.delete("/users/" + profileID)
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
    navigate("/admin");
  }

  const followProfile = async (followedUserID, followedUsername) => {
    await api.post("/users/follow", {
      "userID": followedUserID,
      "username": followedUsername
    })
      .then(function (response) {
        setIsFollowing(true)
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
  }

  const unfollowProfile = async (unfollowedUserID, unfollowedUsername) => {
    await api.post("/users/unfollow", {
      "userID": unfollowedUserID,
      "username": unfollowedUsername
    })
      .then(function (response) {
        console.log(response.data);
        setIsFollowing(false)
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
  }

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="md">
        <CssBaseline />
        <Box>
          <Box
            sx={{
              pt: 8,
              pb: 6,
            }}
          >
            <Container maxWidth="sm">
              <Typography
                component="h1"
                variant="h2"
                align="center"
                color="text.primary"
                gutterBottom
              >
                Profile
              </Typography>
            </Container>
          </Box>
          <Box component="form" noValidate sx={{ mt: 1 }}>
            <Grid container columnSpacing={1.4}>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin='normal'
                  fullWidth
                  disabled
                  name="name"
                  id="name"
                  label="Name"
                  defaultValue={profile.name}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin='normal'
                  fullWidth
                  disabled
                  id="surname"
                  name="surname"
                  label="Surname"
                  defaultValue={profile.surname}
                />
              </Grid>
            </Grid>
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="gender"
              name="gender"
              label="Gender"
              defaultValue={profile.gender}
            />
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="dateOfBirth"
              name="dateOfBirth"
              label="Date of birth"
              defaultValue={Moment(profile.dateOfBirth).utc().format('MMM DD YYYY')}
            />
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="username"
              name="username"
              label="Username"
              defaultValue={profile.username}
              autoFocus
            />
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="nationality"
              name="nationality"
              label="Nationality"
              defaultValue={profile.nationality}
              autoFocus
            />
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="knownLanguages"
              name="knownLanguages"
              label="Languages"
              defaultValue={profile.knownLanguages}
              style={{ marginBottom: 50 + 'px' }}
              autoFocus
            />
            <Grid container>
              <Grid item xs>
              </Grid>
              <Grid item>
              </Grid>
            </Grid>
          </Box>
        </Box>
        {localStorage.getItem("userID") !== profileID && localStorage.getItem("role") !== "admin" ?
          (!isFollowing ?
            <Button
              fullWidth
              variant="contained"
              color='success'
              sx={{marginBottom: 5}}
              onClick={() => { followProfile(profile._id, profile.username) }}>Follow
            </Button>
            :
            <Button
              fullWidth
              variant="contained"
              color='error'
              sx={{marginBottom: 5}}
              onClick={() => { unfollowProfile(profile._id, profile.username) }}>Unfollow
            </Button>) : <></>
        }
        {localStorage.getItem("role") === "admin" ? (
          <Button fullWidth
            variant="contained"
            color='error'
            onClick={() => { deleteProfile(profile._id) }}>Delete Profile</Button>
        ) : <></>
        }
        {(localStorage.getItem("role") === "admin" || localStorage.getItem("userID") === profile._id) ? (
          <EditProfileModal id={profile._id} name={profile.name} surname={profile.surname} gender={profile.gender} dateOfBirth={profile.dateOfBirth} nationality={profile.nationality} knownLanguages={profile.knownLanguages} />
        ) : <></>
        }
      </Container>
      {localStorage.getItem("userID") === profileID || localStorage.getItem("role") === "admin" ?
        <>
          <Box
            sx={{
              pt: 8,
              pb: 6,
            }}
          >
            <Container maxWidth="sm">
              <Typography
                component="h1"
                variant="h2"
                align="center"
                color="text.primary"
                gutterBottom
              >
                Reservations
              </Typography>
            </Container>
          </Box>
          <Container maxWidth="md">
            <TableContainer component={Paper} style={{ marginBottom: 50 + 'px', maxHeight: "30rem", overflow: "auto" }}>
              <Table sx={{ minWidth: 650 }} size="small">
                <TableHead>
                  <TableRow>
                    <TableCell align="left" style={{ fontWeight: 'bold' }}>ID</TableCell>
                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Type</TableCell>
                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Start Date</TableCell>
                    <TableCell align="center" style={{ fontWeight: 'bold' }}>End Date</TableCell>
                    <TableCell align="right" style={{ fontWeight: 'bold' }} />
                    <TableCell align="right" style={{ fontWeight: 'bold' }} />
                  </TableRow>
                </TableHead>
                <TableBody>
                  {profile.reservations.map((item) => (
                    <TableRow key={item._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }} style={{ marginBottom: 50 + 'px', maxHeight: "30rem", overflow: "auto" }}>
                      <TableCell align="left">
                        <Link style={{ cursor: "pointer" }} onClick={() => navigate("/" + item.destinationType + "/" + item.destinationID)}>
                          {item._id}
                        </Link>
                      </TableCell>
                      <TableCell align="center">{item.destinationType}</TableCell>
                      <TableCell align="center">{Moment(item.startDate).utc().format('MMM DD YYYY')}</TableCell>
                      {item.endDate ?
                        <TableCell align="center">{Moment(item.endDate).utc().format('MMM DD YYYY')}</TableCell>
                        :
                        <TableCell align="center" />
                      }
                      <TableCell align='right'>
                        <DeleteIcon color='error' style={{ cursor: "pointer" }} onClick={() => { deleteReservation(item._id) }} />
                      </TableCell>
                      {profileID === localStorage.getItem("userID") ?
                        (<TableCell align='right'>
                          <EditReservationModal reservation={item} />
                        </TableCell>
                        ) : <></>}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </Container>
          <Box
            sx={{
              py: 3,
              px: 2,
              mt: 'auto',
            }}
          >
          </Box>
        </> : <></>
      }
      <Container maxWidth='md'>
        <Grid container columnSpacing={2}>
          {/* Tabella persone seguite */}
          <Grid item xs={4} sm={6}>
            <Container maxWidth="sm">
              <Typography
                component="h3"
                variant="h5"
                align="center"
                color="text.primary"
                gutterBottom
              >
                Followed Users
              </Typography>
            </Container>
            <TableContainer component={Paper} style={{ marginBottom: 50 + 'px', maxHeight: "30rem", overflow: "auto" }} >
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell align="left" style={{ fontWeight: 'bold' }}>ID</TableCell>
                    <TableCell align="right" style={{ fontWeight: 'bold' }}>Username</TableCell>
                  </TableRow>
                </TableHead>
                <tbody>
                  {listFollowedUsers && listFollowedUsers.map((item, index) => (
                    <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                      <TableCell align="left">
                        <Link style={{ cursor: 'pointer' }} onClick={() => { navigate("/profile/" + item.userID); window.location.reload(false); }}>
                          {item.userID}
                        </Link>
                      </TableCell>
                      <TableCell align="right">{item.username}</TableCell>
                    </TableRow>
                  ))}
                </tbody>
              </Table>
            </TableContainer>
          </Grid>
          {/* Tabella annunci piaciuti */}
          <Grid item xs={4} sm={6}>
            <Container maxWidth="sm">
              <Typography
                component="h3"
                variant="h5"
                align="center"
                color="text.primary"
                gutterBottom
              >
                Liked Advs
              </Typography>
            </Container>
            <TableContainer component={Paper} style={{ marginBottom: 50 + 'px', maxHeight: "30rem", overflow: "auto" }} >
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell align="left" style={{ fontWeight: 'bold' }}>ID</TableCell>
                    <TableCell align="right" style={{ fontWeight: 'bold' }}>Name</TableCell>
                  </TableRow>
                </TableHead>
                <tbody>
                  {listLikedAcc && listLikedAcc.map((item, index) => (
                    <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                      <TableCell align="left">
                        <Link style={{ cursor: 'pointer' }} onClick={() => navigate("/accommodation/" + item.accommodationID)} >
                          {item.accommodationID}
                        </Link>
                      </TableCell>
                      <TableCell align="right">{item.name}</TableCell>
                    </TableRow>
                  ))}
                  {listLikedAct && listLikedAct.map((item, index) => (
                    <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                      <TableCell align="left">
                        <Link style={{ cursor: 'pointer' }} onClick={() => navigate("/activity/" + item.activityID)}>
                          {item.activityID}
                        </Link>
                      </TableCell>
                      <TableCell align="right">{item.name}</TableCell>
                    </TableRow>
                  ))}
                </tbody>
              </Table>
            </TableContainer>
          </Grid>
          {/* Tabella annunci piaciuti in comune */}
          {localStorage.getItem("userID") !== profileID ?
            <>
              <Container maxWidth='lg'>
                <Container maxWidth="sm">
                  <Typography
                    component="h3"
                    variant="h5"
                    align="center"
                    color="text.primary"
                    gutterBottom
                  >
                    Common Liked Advs
                  </Typography>
                </Container>
                <TableContainer component={Paper} style={{ marginBottom: 50 + 'px', maxHeight: "30rem", overflow: "auto" }} >
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell align="left" style={{ fontWeight: 'bold' }}>ID</TableCell>
                        <TableCell align="right" style={{ fontWeight: 'bold' }}>Name</TableCell>
                      </TableRow>
                    </TableHead>
                    <tbody>
                      {listCommonLikedAcc && listCommonLikedAcc.map((item, index) => (
                        <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                          <TableCell align="left">
                            <Link style={{ cursor: 'pointer' }} onClick={() => navigate("/accommodation/" + item.accommodationID)}>
                              {item.accommodationID}
                            </Link>
                          </TableCell>
                          <TableCell align="right">{item.name}</TableCell>
                        </TableRow>
                      ))}
                      {listCommonLikedAct && listCommonLikedAct.map((item, index) => (
                        <TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                          <TableCell align="left">
                            <Link style={{ cursor: 'pointer' }} onClick={() => navigate("/activity/" + item.accommodationID)}>
                              {item.activityID}
                            </Link>
                          </TableCell>
                          <TableCell align="right">{item.name}</TableCell>
                        </TableRow>
                      ))}
                    </tbody>
                  </Table>
                </TableContainer>
              </Container>
            </> : <></>
          }
        </Grid>
      </Container>
      <Box
        sx={{
          py: 3,
          px: 2,
          mt: 'auto',
        }}
      />
    </ThemeProvider>
  );
}

export default Profile;