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
import api from "../api/api";
import { useNavigate } from 'react-router-dom';
import useAuth from '../hooks/useAuth';


const theme = createTheme();

const Search = () => {
    const [last_id, setLast_id] = React.useState(null);
    const [first_id, setFirst_id] = React.useState(null);
    const [page, setPage] = React.useState(1);
    const [lastPage, setLastPage] = React.useState(null);  const { auth } = useAuth();
    const navigate = useNavigate();
    const [search, setSearch] = React.useState(null);
    const [startDate , setStartDate] = React.useState(null);
    const [endDate , setEndDate] = React.useState(null);
    const [city, setCity] = React.useState(null);
    const [guests , setGuests] = React.useState(null);
    const [type, setType] = React.useState("accomodations");
    const handleChange = (event) => {
    setType(event.target.value);
    };


  const handleSearch = (event) => {
      event.preventDefault();
      setPage(1);
      setLastPage(false)
      const form = new FormData(event.currentTarget);
      const city = form.get('city');
      const guests = form.get('numberOfPeople');
      const formStartDate = form.get('startDate');
      const formEndDate = form.get('endDate');
      setStartDate(formStartDate);
      setEndDate(formEndDate);
      setCity(city)
      setGuests(guests)
      const url ="?startDate=" + formStartDate + "&endDate=" + formEndDate + "&city=" + city + "&guestsNumber=" + guests + "&index=";
      console.log(url);

      api.get("/" + type + url , {headers:{"Authorization":JSON.stringify(auth)}})
      .then(function (response) {
            setSearch(response.data);
              setFirst_id(response.data[0]._id);
              setLast_id("637bb280945bed1e66467434");
          response.data.forEach((elem, index) => {
            console.log("ID" + index, elem._id);
          })
             // console.log(response.data);
      })
      .catch(function (error) {
        console.log(error);
      });
  };

    const handlePreviousPage = () => {
        setPage(page-1)
        const url ="?startDate=" + startDate + "&endDate=" + endDate + "&city=" + city + "&guestsNumber=" + guests + "&index=" + first_id + "&direction=previous";
        console.log(url);
        api.get("/" + type + url)
            .then(function (response) {
                setSearch(response.data);
                setLastPage(false)
                if (response && response.data.length > 0 ) {
                    setLast_id(response.data[0]._id);
                    setFirst_id(response.data[response.data.length - 1]._id);
                }
                //console.log(response.data);
                console.log(first_id)
                console.log(last_id)
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    const handleNextPage = () => {
        const url ="?startDate=" + startDate + "&endDate=" + endDate + "&city=" + city + "&guestsNumber=" + guests + "&index=" + last_id + "&direction=next";
        console.log(url);
        api.get("/" + type + url)
            .then(function (response) {
                if (response && response.data.length > 0 ) {
                    console.log("length response:" , response.data.length)
                    setLast_id(response.data[response.data.length - 1]._id);
                    setFirst_id(response.data[0]._id);
                    setSearch(response.data);
                    setPage(page+1);
                    response.data.forEach((elem, index) => {
                        console.log("ID" + index, elem._id);
                    })
                }
                else{
                    setLastPage(true)
                }
                console.log(response.data);
                console.log(first_id)
                console.log(last_id)
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    const handleFirstPage = () => {
        setPage(1);
        const url ="?startDate=" + startDate + "&endDate=" + endDate + "&city=" + city + "&guestsNumber=" + guests + "&index=";

        console.log(url);
        api.get("/" + type + url)
            .then(function (response) {
                setSearch(response.data);
                setLast_id(response.data[response.data.length - 1]._id);
                setFirst_id(0);
                //console.log(response.data);
                setLastPage(false)
            })
            .catch(function (error) {
                console.log(error);
                console.log(first_id)
                console.log(last_id)
            });

    };

    const emptyRows =
        page > 1 ? Math.max(0, 2 - search ? search.length : 0) : 0;


  //Vari setter per gestione di form e url
  let setter = '';
  let hideNumberOfPerson = true
  let hideEndDate = true
  let hideStartDate = true

  if (type == 'accomodations') {
    setter = 'accomodation'
    hideNumberOfPerson = false
    hideEndDate = false
    hideStartDate = false
  } else {
    setter = 'activity'
    hideNumberOfPerson = true
    hideEndDate = true
    hideStartDate = false
  }


  const [page, setPage] = React.useState(0);
  const [itemPerPage, setItemPerPage] = React.useState(15);


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
                  <MenuItem value={'activities'}>Activities</MenuItem>
                  <MenuItem value={'accomodations'}>Accomodations</MenuItem>
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
                  disabled={hideStartDate}
                />
              </Grid>

              <Grid item xs={6} sm={2}>
                <TextField
                  fullWidth
                  id="endDate"
                  name="endDate"
                  type="date"
                  disabled={hideEndDate}
                />
              </Grid>

              <Grid item xs={4} sm={2}>
                <TextField
                  fullWidth
                  id="numberOfPeople"
                  label="Number of people"
                  name="numberOfPeople"
                  type="number"
                  disabled={hideNumberOfPerson}
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
          <Container>
          {/* End hero unit */}
          <Grid container spacing={4}>
              { search && search.map((item) => (
                        <Grid item key={item._id} xs={12} sm={6} md={4}>
                            <Card
                            sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                            >
                                <CardContent sx={{ flexGrow: 1 }}>
                                    <Typography gutterBottom variant="h5" component="h2">
                                        {item.name}
                                    </Typography>
                                </CardContent>
                                <CardMedia
                                component="img"
                                src={`data:image/jpeg;base64,${item.mainPicture}`}
                                />
                                <CardContent sx={{ flexGrow: 1 }}>
                                    <Typography variant='span'>
                                        <b>{item.location.city}</b>
                                        <br/>
                                        <i>{item.location.address}</i>
                                        <br/>
                                            {item.price}€
                                    </Typography>
                                </CardContent>
                                <CardActions>
                                    <Button fullWidth onClick={()=>{navigate("/"+setter+"/"+item._id+"?startDate="+startDate+"&endDate="+endDate)}}>View</Button>
                                </CardActions>
                            </Card>
                        </Grid>
                    ))}
              <Grid>
                  {page !== 1 ? <Button onClick={() => {handlePreviousPage()}}>Previous</Button> : <></>}
                  {lastPage != null && !lastPage ? <Button onClick={() => {handleNextPage()}}>Next</Button> : <></>}
                  {page !== 1 ? <Button onClick={() => {handleFirstPage()}}> First</Button> : <></>}
              </Grid>
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

export default Search;