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
import {useNavigate, useParams, useSearchParams} from "react-router-dom";
import api from "../api/api";

function createDataActivities(
  title,
  date,
  state
) {
  return { title, date, state};
}

const rowsActivities = [
  createDataActivities('Disco', '4/10/2022', 'Complited'),
  createDataActivities('Socker', '11/11/2022', 'Complited'),
  createDataActivities('Baseball', '24/11/2022', 'To do')
];

function createDataAccomodations(
  title,
  date,
  state
) {
  return { title, date, state};
}

const rowsAccomodations = [
  createDataAccomodations('Turin', '25/10/2022', 'Complited'),
  createDataAccomodations('Rome', '11/11/2022', 'Complited'),
  createDataAccomodations('Milan', '23/12/2022', 'To do')
];


const theme = createTheme();

export default function Profile() {
  const [searchParams] = useSearchParams();
  const {userID} = useParams();
  const [user, setUser] = React.useState(null);

  React.useEffect(() => {
    api.get("/users/"+ userID)
        .then(function (response) {
          setUser(response.data);
          console.log(response.data);
        })
        .catch(function (error) {
          console.log(error);
        });
  }, []);

  if(user!=null)
    return(
      <ThemeProvider theme={theme}>
        <Container component="main" maxWidth="md">
          <CssBaseline/>
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
            <Box component="form" noValidate sx={{mt: 1}}>
              <Grid container columnSpacing={1.4}>
                <Grid item xs={12} sm={6}>
                  <TextField
                      disabled
                      fullWidth
                      label={user.name}
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                      disabled
                      fullWidth
                      label={user.surname}
                  />
                </Grid>
              </Grid>
              <TextField
                  margin="normal"
                  disabled
                  fullWidth
                  label={user.gender}
              />
              <TextField
                  margin="normal"
                  disabled
                  fullWidth
                  label={user.dateOfBirth}
              />
              <TextField
                  margin="normal"
                  disabled
                  fullWidth
                  label={user._id}
                  autoFocus
                  style={{marginBottom: 50 + 'px'}}
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
        <Container maxWidth="md">
          <TableContainer component={Paper} style={{marginBottom: 50 + 'px'}}>
            <Table sx={{minWidth: 650}} size="small" aria-label="a dense table">
              <TableHead>
                <TableRow>
                  <TableCell style={{fontWeight: 'bold'}}>
                    Accomodations
                  </TableCell>
                  <TableCell align="right" style={{fontWeight: 'bold'}}>Title</TableCell>
                  <TableCell align="right" style={{fontWeight: 'bold'}}>Date</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rowsAccomodations.map((row) => (
                    <TableRow
                        key={row.title}
                        sx={{'&:last-child td, &:last-child th': {border: 0}}}
                    >
                      <TableCell component="th" scope="row">
                        {row.title}
                      </TableCell>
                      <TableCell align="right">{row.date}</TableCell>
                      <TableCell align="right">{row.state}</TableCell>
                    </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          <TableContainer component={Paper}>
            <Table sx={{minWidth: 650}} size="small" aria-label="a dense table">
              <TableHead>
                <TableRow>
                  <TableCell style={{fontWeight: 'bold'}}>Activities</TableCell>
                  <TableCell align="right" style={{fontWeight: 'bold'}}>Title</TableCell>
                  <TableCell align="right" style={{fontWeight: 'bold'}}>Date</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {rowsActivities.map((row) => (
                    <TableRow
                        key={row.title}
                        sx={{'&:last-child td, &:last-child th': {border: 0}}}
                    >
                      <TableCell component="th" scope="row">
                        {row.title}
                      </TableCell>
                      <TableCell align="right">{row.date}</TableCell>
                      <TableCell align="right">{row.state}</TableCell>
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