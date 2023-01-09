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
import api from "../utility/api";
import { useNavigate, useSearchParams} from 'react-router-dom';


const theme = createTheme();

const Search = () => {
  const [searchParams] = useSearchParams();
  const [last_id, setLast_id] = React.useState(null);
  const [first_id, setFirst_id] = React.useState(null);
  const [page, setPage] = React.useState(1);
  const [lastPage, setLastPage] = React.useState(null);
  const [search, setSearch] = React.useState(null);
  const [startDate, setStartDate] = React.useState(null);
  const [endDate, setEndDate] = React.useState(null);
  const [city, setCity] = React.useState(searchParams.get("city") ? searchParams.get("city") : "");
  const [guests, setGuests] = React.useState("");
  const [type, setType] = React.useState(searchParams.get("type") ? searchParams.get("type") : "accommodations");
  const [setter, setSetter] = React.useState("accommodation");
  const today = new Date();
  const date = today.getFullYear() + '-' + ((today.getMonth() + 1) > 10 ? (today.getMonth() + 1) : ('0' + (today.getMonth() + 1))) + (today.getDate() > 10 ? today.getDate() > 10 : ('-0' + today.getDate()));
  const navigate = useNavigate();


  const handleChange = (event) => {
    setType(event.target.value);
    if(event.target.value === "accommodations")
      setSetter("accommodation")
    else
      setSetter("activity")
  };

  const onChangeStartDate = (event) => {
    setStartDate(event.target.value);
    console.log(event.target.value)
  }

  const onChangeEndDate = (event) => {
    setEndDate(event.target.value);
    console.log(event.target.value)
  }

  const handleSearch = (event) => {
    event.preventDefault();
    setPage(1);
    const form = new FormData(event.currentTarget);
    const city = form.get('city');
    const guests = form.get('numberOfPeople');
    const formStartDate = form.get('startDate');
    const formEndDate = form.get('endDate');
    setStartDate(formStartDate);
    setEndDate(formEndDate);
    setCity(city)
    setGuests(guests)
    const url = "?startDate=" + formStartDate + "&endDate=" + formEndDate + "&city=" + city + "&guestsNumber=" + guests + "&index=";

    api.get("/" + type + url)
      .then(function (response) {
        setSearch(response.data);
        if (response && response.data.length > 0) {
          setFirst_id(response.data[0]._id);
          setLast_id(response.data[response.data.length - 1]._id);
          setLastPage(false)
        }
        else{
          setLastPage(true)
          setSearch(null)
        }
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
  };

  const handlePreviousPage = async () => {
    setPage(page - 1)
    const url = "?startDate=" + startDate + "&endDate=" + endDate + "&city=" + city + "&guestsNumber=" + guests + "&index=" + first_id + "&direction=previous";
    await api.get("/" + type + url)
      .then(function (response) {
        setSearch(response.data);
        setLastPage(false)
        if (response && response.data.length > 0) {
          setLast_id(response.data[0]._id);
          setFirst_id(response.data[response.data.length - 1]._id);
        }
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
  };

  const handleNextPage = async () => {
    const url = "?startDate=" + startDate + "&endDate=" + endDate + "&city=" + city + "&guestsNumber=" + guests + "&index=" + last_id + "&direction=next";
    await api.get("/" + type + url)
      .then(function (response) {
        if (response && response.data.length > 0) {
          setLast_id(response.data[response.data.length - 1]._id);
          setFirst_id(response.data[0]._id);
          setSearch(response.data);
          setPage(page + 1);
        }
        else {
          setLastPage(true)
        }
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });
  };

  const handleFirstPage = async () => {
    setPage(1);
    const url = "?startDate=" + startDate + "&endDate=" + endDate + "&city=" + city + "&guestsNumber=" + guests + "&index=";

    await api.get("/" + type + url)
      .then(function (response) {
        setSearch(response.data);
        setLast_id(response.data[response.data.length - 1]._id);
        setFirst_id(0);
        setLastPage(false)
      })
      .catch(function (error) {
        alert("Ops, something went wrong :(" + "\n" + error);
      });

  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <main>
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
                  <MenuItem value={'accommodations'}>Accommodations</MenuItem>
                </Select>
              </Grid>
              <Grid item xs={6} sm={4}>
                <TextField
                  fullWidth
                  name="city"
                  id="city"
                  label="City"
                  defaultValue={city}
                  multiline
                />
              </Grid>
              <Grid item xs={6} sm={2}>
                <TextField
                  fullWidth
                  id="startDate"
                  name="startDate"
                  type="date"
                  onChange={onChangeStartDate}
                  InputProps={{ inputProps: { min:`${date}`, max: endDate ? `${endDate}` : ""}}}
                />
              </Grid>
              {type === "accommodations" ? (<Grid item xs={6} sm={2}>
                <TextField
                  fullWidth
                  id="endDate"
                  name="endDate"
                  type="date"
                  onChange={onChangeEndDate}
                  InputProps={{ inputProps: { min:`${startDate}`, max:""}, }}
                />
              </Grid>) : <></>}
              {type === "accommodations" ?
              <Grid item xs={4} sm={2}>
                <TextField
                  fullWidth
                  id="numberOfPeople"
                  label="Number of people"
                  name="numberOfPeople"
                  type="number"
                />
              </Grid> : <></>}
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
          <Grid container spacing={4}>
            {search && search.map((item) => (
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
                      <br />
                      <i>{item.location.address}</i>
                      <br />
                      {item.price}€
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <Button
                        fullWidth
                        onClick={() => { navigate("/" + setter + "/" + item._id + "?startDate=" + startDate + "&endDate=" + endDate + "&guests=" + guests) }}
                        variant="contained"
                        color='info'
                    >
                      View
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>

          {/* Separatore */}
          <Box
            sx={{
              bgcolor: 'background.paper',
              pt: 8,
              pb: 6,
            }}
          />


           
          {/* Bottoni pagine */}
          <Grid container columnSpacing={1.4}>
            <Grid item xs={4} sm={4}>
            {page !== 1 ? 
              <Button 
                type="submit" 
                fullWidth 
                variant="contained" 
                sx={{ mt: 3, mb: 2 }} 
                onClick={() => { handlePreviousPage() }}>Previous Page</Button> : <></>}
            </Grid>
            
            <Grid item xs={4} sm={4}>
              {lastPage != null && !lastPage ? 
              <Button
                type="submit" 
                fullWidth 
                variant="contained" 
                sx={{ mt: 3, mb: 2 }} 
                onClick={() => { handleNextPage() }}>Next Page</Button> : <></>}
            </Grid>
            
            <Grid item xs={4} sm={4}>
            {page !== 1 ? 
              <Button
                type="submit" 
                fullWidth 
                variant="contained" 
                sx={{ mt: 3, mb: 2 }} 
                onClick={() => { handleFirstPage() }}>First Page</Button> : <></>}
            </Grid>
          </Grid>
            


        </Container>
        <Box
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