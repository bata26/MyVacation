import {useState} from 'react';
import Avatar from '@mui/material/Avatar';
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { FormControl } from '@mui/material';
import FormLabel from '@mui/material/FormLabel';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import api from '../api/api'
import { useNavigate } from "react-router-dom";


const theme = createTheme();
const REGISTER_URL = '/register';

const SignUp = () => {
    const [errMsg, setErrMsg] = useState('');
    let navigate = useNavigate();

    const handleSubmit = async (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        console.log({
            name: data.get('name'),
            surname: data.get('surname'),
            gender: data.get('gender'),
            dateOfBirth: data.get('dateOfBirth'),
            username: data.get('username'),
            password: data.get('password'),
        });
        try {
          const response = await api.post(REGISTER_URL, JSON.stringify({
                  name: data.get('name'),
                  surname: data.get('surname'),
                  gender: data.get('gender'),
                  dateOfBirth: data.get('dateOfBirth'),
                  username: data.get('username'),
                  password: data.get('password'),
              }),
              {
                  headers: { 'Content-Type': 'application/json' },
                  withCredentials: true
              }
          );
          console.log(response?.data);
          //console.log(response?.accessToken);
          console.log(JSON.stringify(response));
          //clear state and controlled inputs
          //need value attrib on inputs for this
          navigate("/", { replace: true });
        } catch (err) {
          if (!err?.response) {
              setErrMsg('No Server Response');
          } //else if (err.response?.status === 409) {
              //setErrMsg('Username Taken')} else
          else{
              setErrMsg('Registration Failed')
          }
        }
    };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'secondary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign Up
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
              <Grid container columnSpacing={1.4}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                    autoComplete="given-name"
                    name="firstName"
                    required
                    fullWidth
                    id="name"
                    label="First Name"
                    autoFocus
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                    required
                    fullWidth
                    id="surname"
                    label="Last Name"
                    name="lastName"
                    autoComplete="family-name"
                    />
                  </Grid>
              </Grid>
              <FormControl>
                  <FormLabel id="gender" margin='normal'>Gender</FormLabel>
                  <RadioGroup
                  aria-labelledby="gender"
                  defaultValue="male"
                  name="radio-buttons-group"
                  row
                  >
                    <FormControlLabel value="male" control={<Radio />} label="Male" />
                    <FormControlLabel value="female" control={<Radio />} label="Female" />
                    <FormControlLabel value="other" control={<Radio />} label="Other" />
                  </RadioGroup>
              </FormControl>
              <TextField
              margin="normal"
              required
              fullWidth
              name="dateOfBirth"
              label="Date of birth"
              type="dateOfBirth"
              id="dateOfBirth"
              autoComplete="dateOfBirth"
              autoFocus
              />
              <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              autoComplete="username"
              autoFocus
              />
              <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              autoComplete="current-password"
              />
              <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
              >
                Sign Up
              </Button>
              <Grid container>
                <Grid item xs>
                </Grid>
                <Grid item>
                </Grid>
              </Grid>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default SignUp;