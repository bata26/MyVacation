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

import api from "../api/api";
import { useParams } from 'react-router-dom';
import Moment from 'moment';

function createDataActivities(
  nameOrCategory,
  city,
  date
) {
  return { nameOrCategory, city, date};
}

const rowsActivities = [
  createDataActivities('Disco', 'Turin', '25/10/2022'),
  createDataActivities('Socker', 'Milan', '11/11/2022'),
  createDataActivities('Baseball', 'Amsterdam', '23/12/2022')
];

function createDataAccomodations(
  nameOrCategory,
  city,
  date
) {
  return { nameOrCategory, city, date};
}

const rowsAccomodations = [
  createDataAccomodations('Flat near the center', 'Turin', '25/10/2022'),
  createDataAccomodations('Five star Hotel', 'Milan', '11/11/2022'),
  createDataAccomodations('Countryside house', 'Amsterdam', '23/12/2022')
];


const theme = createTheme();

const Profile = () => {


  const [profile , setProfile] = React.useState(null);
  const {profileID} = useParams();

  React.useEffect( () => {

    api.get("/users/"+profileID)
    .then(function(response){
      setProfile(response.data);
    })
    .catch(function(error){
      console.log(error);
    });
  } , []);

  if(!profile) return null;


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
          <Box component="form"  noValidate sx={{ mt: 1 }}>
            <Grid container columnSpacing={1.4}>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin='normal'
                  fullWidth
                  disabled
                  id="outlined-disabled"
                  label="Name"
                  defaultValue= {profile.name}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  margin='normal'
                  fullWidth
                  disabled
                  id="outlined-disabled"
                  label="Surname"
                  defaultValue= {profile.surname}
                />
              </Grid>
            </Grid>
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="outlined-disabled"
              label="Gender"
              defaultValue= {profile.gender}
            />
            <TextField
              margin="normal"
              fullWidth
              disabled
              id="outlined-disabled"
              label="Date of birth"
              defaultValue= {Moment().utc(profile.dateOfBirth).format('MMM DD YYYY')}
            />

            <TextField
              margin="normal"
              fullWidth
              disabled
              id="outlined-disabled"
              label="Username"
              defaultValue= {profile.username}
              style={{marginBottom: 50 + 'px'}} 
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
                Prenotations
              </Typography>
            </Container>
          </Box>


      <Container maxWidth="md">
        <TableContainer component={Paper} style={{marginBottom: 50 + 'px'}} >
          <Table sx={{ minWidth: 650 }} size="small">
            <TableHead>
              <TableRow>
                <TableCell style={{fontWeight: 'bold', height: 50 + 'px'}}>
                  Accomodations
                  </TableCell>
                <TableCell align="center" style={{fontWeight: 'bold'}}>City</TableCell>
                <TableCell align="right" style={{fontWeight: 'bold'}}>Date</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rowsAccomodations.map((row) => (
                <TableRow
                  key={row.nameOrCategory}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row" style={{height: 50 + 'px'}}>
                    {row.nameOrCategory}
                  </TableCell>
                  <TableCell align="center">{row.city}</TableCell>
                  <TableCell align="right">{row.date}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} size="small">
            <TableHead>
              <TableRow>
                <TableCell style={{fontWeight: 'bold', height: 50 + 'px'}}>
                  Activities
                </TableCell>
                <TableCell align="center" style={{fontWeight: 'bold'}}>City</TableCell>
                <TableCell align="right" style={{fontWeight: 'bold'}}>Date</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {rowsActivities.map((row) => (
                <TableRow
                  key={row.nameOrCategory}
                  sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                >
                  <TableCell component="th" scope="row" style={{height: 50 + 'px'}}>
                    {row.nameOrCategory}
                  </TableCell>
                  <TableCell align="center">{row.city}</TableCell>
                  <TableCell align="right">{row.date}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
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
}

export default Profile;