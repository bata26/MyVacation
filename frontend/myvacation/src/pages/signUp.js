import { useState } from 'react';
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
import api from '../utility/api'
import { useNavigate } from "react-router-dom";
import Config from '../utility/config';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';



const theme = createTheme();
const REGISTER_URL = '/signup';

const SignUp = () => {
  const [errMsg, setErrMsg] = useState('');
  const [languages, setLanguages] = useState([]);
  const [nationality, setNationality] = useState(null);
  let navigate = useNavigate();

  const handleNationalityChange = (event) => {
    setNationality(event.target.value);
  };

  const handleChange = (event) => {
    const {
      target: { value },
    } = event;
    setLanguages(value);
  };


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
      languages: data.get('password'),
      nationality: data.get('nationality'),
    });
    try {
      const response = await api.post(REGISTER_URL, JSON.stringify({
        name: data.get('name'),
        surname: data.get('surname'),
        gender: data.get('gender'),
        dateOfBirth: new Date(data.get('dateOfBirth')),
        username: data.get('username'),
        password: data.get('password'),
        knownLanguages: languages,
        nationality: data.get('nationality')
      }),
        {
          headers: { 'Content-Type': 'application/json' },
          withCredentials: true
        }
      );
      console.log(response?.data);
      console.log(JSON.stringify(response));
      navigate("/signin", { replace: true });
    } catch (err) {
      if (!err?.response) {
        setErrMsg('No Server Response');
      } else {
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
                  //autoComplete="given-name"
                  name="name"
                  required
                  fullWidth
                  id="name"
                  label="Name"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="surname"
                  label="Surname"
                  name="surname"
                  //autoComplete="family-name"
                />
              </Grid>
            </Grid>
            <FormControl>
              <FormLabel id="gender" margin='normal'>Gender</FormLabel>
              <RadioGroup
                aria-labelledby="gender"
                defaultValue="male"
                name="gender"
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
              type="date"
              id="dateOfBirth"
              //autoComplete="dateOfBirth"
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              id="username"
              label="Username"
              name="username"
              //autoComplete="username"
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
              //autoComplete="current-password"
            />
            <InputLabel id="demo-simple-select-label">Age</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="nationality"
              label="Nationality"
              fullWidth
              onChange={handleNationalityChange}
              required
            >
              {Config.NATIONALITY_LIST.map((item, index) => {
                return <MenuItem value={index}>{item}</MenuItem>
              })}
            </Select>
            <InputLabel id="demo-simple-select-label">Languages</InputLabel>
            <Select
              labelId="demo-simple-select-label"
              id="language"
              label="Languages"
              multiple
              value={languages}
              onChange={handleChange}
              fullWidth
              required
            >
              {Config.LANGUAGE_LIST.map((item, index) => {
                return <MenuItem key={index} value={index}>{item}</MenuItem>
              })}
            </Select>
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