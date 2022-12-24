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
import { useNavigate, useSearchParams } from 'react-router-dom';
import Button from '@mui/material/Button';


const theme = createTheme();

const Profile = () => {
  const [profile, setProfile] = React.useState(null);
  let [reservations, setReservations] = React.useState([]);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  //TODO FIXARE STA ROBA
  const profileID = (searchParams.get("userId") != null && localStorage.getItem("role") === "admin") ? searchParams.get("userId") : localStorage.getItem("userID");

  React.useEffect(() => {
    //Richiesta per recuperare le informazioni dell'utente
    api.get("/users/" + profileID)
      .then(function (response) {
        setProfile(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });

    //Richiesta per recuperare le prenotazioni
    api.get("/reservations/" + profileID)
      .then(function (response) {
        setReservations(response.data);
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  }, []);

  if (!profile) return null;

  //Metodo per eliminare reservation
  const deleteReservation = async (reservationID) => {
    await api.delete("/reservations/" + reservationID)
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
      window.location.reload(false);
    }
    const deleteProfile = async (profileID) => {
      await api.delete("/users/" + profileID)
      .then(function (response) {
        console.log(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
      navigate("/admin");
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
                  id="outlined-disabled"
                  label="Name"
                  defaultValue={profile.name}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin='normal'
                  fullWidth
                  disabled
                  id="outlined-disabled"
                  label="Surname"
                  defaultValue={profile.surname}
                />
              </Grid>
            </Grid>
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="outlined-disabled"
              label="Gender"
              defaultValue={profile.gender}
            />
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="outlined-disabled"
              label="Date of birth"
              defaultValue={Moment(profile.dateOfBirth).utc().format('MMM DD YYYY')}
            />
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="outlined-disabled"
              label="Username"
              defaultValue={profile.username}
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
        {localStorage.getItem("role") == "admin" ? (
          <Button fullWidth
            variant="contained"
            color='error'
            onClick={() => { deleteProfile(profile._id) }}>elimina profilo</Button>
        ) : <></>
        }

      </Container>

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
        <TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
          <Table sx={{ minWidth: 650 }} size="small">
            <TableHead>
              <TableRow>
                <TableCell align="left" style={{ fontWeight: 'bold' }}>ID</TableCell>
                <TableCell align="center" style={{ fontWeight: 'bold' }}>Type</TableCell>
                <TableCell align="center" style={{ fontWeight: 'bold' }}>Start Date</TableCell>
                <TableCell align="center" style={{ fontWeight: 'bold' }}>End Date</TableCell>
                <TableCell align="right" style={{ fontWeight: 'bold' }}></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {reservations.map((item) => (
                <TableRow key={item._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                  <TableCell align="left">{item._id}</TableCell>
                  <TableCell align="center">{item.destinationType}</TableCell>
                  <TableCell align="center">{Moment(item.startDate).utc().format('MMM DD YYYY')}</TableCell>
                  {item.endDate ?
                    <TableCell align="center">{Moment(item.endDate).utc().format('MMM DD YYYY')}</TableCell>
                    :
                    <TableCell align="center"></TableCell>
                  }
                  <TableCell align='right'>
                    <DeleteIcon color='error' style={{ cursor: "pointer" }} onClick={() => { deleteReservation(item._id) }}></DeleteIcon>
                  </TableCell>
                  {profileID === localStorage.getItem("userID") ?
                    (<TableCell align='right'>
                      <EditReservationModal type={item.destinationType} endDateProp={item.endDate} startDateProp={item.startDate} reservationId={item._id} destinationID={item.destinationID}></EditReservationModal>
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
    </ThemeProvider>
  );
}

export default Profile;