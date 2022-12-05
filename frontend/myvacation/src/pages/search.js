import * as React from 'react';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CssBaseline from '@mui/material/CssBaseline';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { TextField } from '@mui/material';
import MenuItem from '@mui/material/MenuItem';
import Select from '@mui/material/Select';


const handleSearch = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log({
      type: data.get('type'),
      city: data.get('city'),
      startDate: data.get('startDate'),
      endDate: data.get('endDate'),
      numberOfPeople: data.get('numberOfPeople'),
    });
};


const cards = [1, 2, 3, 4, 5, 6, 7, 8, 9];

const theme = createTheme();

export default function Search() {
    const [type, setType] = React.useState('');
    const handleChange = (event) => {
        setType(event.target.value);
    };


  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <main>
        {/* Hero unit */}
        <Box
          sx={{
            bgcolor: 'background.paper',
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
              Search
            </Typography>
          </Container>
        </Box>



        {/* Inizio blocco ricerca */}


        <Container>
        <CssBaseline />
            <Box component="form" onSubmit={handleSearch} noValidate sx={{ mt: 1 }}>
              <Grid container columnSpacing={1.4}>
                <Grid item xs={4} sm={2}>
                    <Select
                        fullWidth
                        id='type'
                        name='type'
                        value={type}
                        onChange={handleChange}
                    >
                        <MenuItem value={'activity'}>Activity</MenuItem>
                        <MenuItem value={'accomodation'}>Accomodation</MenuItem>
                    </Select>
                </Grid>
                <Grid item xs={6} sm={4}>
                    <TextField
                    fullWidth
                    name="city"
                    id="city"
                    label="City"
                    />
                </Grid>
                <Grid item xs={6} sm={2}>
                    <TextField
                    fullWidth
                    id="startDate"
                    name="startDate"
                    type="date"
                    />
                </Grid>

                <Grid item xs={6} sm={2}>
                    <TextField
                    fullWidth
                    id="endDate"
                    name="endDate"
                    type="date"
                    />
                </Grid>

                <Grid item xs={4} sm={2}>
                    <TextField
                    fullWidth
                    id="numberOfPeople"
                    label="Number of people"
                    name="numberOfPeople"
                    type="number"
                    />
                </Grid>

            </Grid>
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              Search
            </Button>
          </Box>
      </Container>


        {/* Separatore */}


      <Box
          sx={{
            bgcolor: 'background.paper',
            pt: 8,
            pb: 6,
          }}
        />


        {/* Inizio risultati ricerca */}



        <Container >
          {/* End hero unit */}
          <Grid container spacing={4}>
            {cards.map((card) => (
              <Grid item key={card} xs={12} sm={6} md={4}>
                <Card
                  sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                >
                  <CardContent sx={{ flexGrow: 1 }}>

                    <Typography gutterBottom variant="h5" component="h2">
                      Title
                    </Typography>

                  </CardContent>
                    <CardMedia
                    component="img"
                    image="https://picsum.photos/200"
                    alt="random"
                  />
                  <CardContent sx={{ flexGrow: 1 }}>
                    <Typography>
                      This is the description of the activity or the accomodation
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button fullWidth>View</Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
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
      </main>
    </ThemeProvider>
  );
}