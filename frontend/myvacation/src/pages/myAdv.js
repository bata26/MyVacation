import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import { Link, Typography } from '@mui/material';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import api from "../utility/api";
import { useNavigate } from 'react-router-dom';
import Select from "@mui/material/Select";
import MenuItem from "@mui/material/MenuItem";

const theme = createTheme();

const MyAdv = () => {

    const profileID = localStorage.getItem("userID");
    const navigate = useNavigate();
    const [monthReservation, setMonthReservation] = React.useState([]);
    const [accommodations, setAccommodations] = React.useState([]);
    const [activities, setActivities] = React.useState([]);
    let selectedCities = [];
    const [stateCities, setStateCities] = React.useState([]);
    const [city, setCity] = React.useState([]);


    React.useEffect(() => {
        setCity(1);
        //Richiesta per recuperare le accommodations dell'utente
        api.get("/myadvacc/" + profileID)
            .then(function (response) {
                setAccommodations(response.data);
                response.data.map((item) => {
                    if (!selectedCities.includes(item.location.city))
                        selectedCities.push(item.location.city);
                });
            })
            .catch(function (error) {
                alert("Ops, something went wrong :(" + "\n" + error);
            }
            );

        //Richiesta per recuperare le activities dell'utente
        api.get("/myadvact/" + profileID)
            .then(function (response) {
                setActivities(response.data);
                response.data.map((item) => {
                    if (!selectedCities.includes(item.location.city))
                        selectedCities.push(item.location.city);
                });
            })
            .catch(function (error) {
                alert("Ops, something went wrong :(" + "\n" + error);
            }
            );


        //Richiesta per recuperare le activities dell'utente
        api.get("/analytics/monthReservations")
            .then(function (response) {
                setMonthReservation(response.data);
                console.log(monthReservation);
            })
            .catch(function (error) {
                alert("Ops, something went wrong :(" + "\n" + error);
            }
            );
        setStateCities(selectedCities);
        setCity(stateCities[0]);
    }, []);

    const handleChange = (event) => {
        setCity(event.target.value);
    }

    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="md">
                <CssBaseline />

                <Box sx={{ pt: 8, pb: 6 }}>
                    <Container maxWidth="sm">
                        <Typography
                            component="h1"
                            variant="h2"
                            align="center"
                            color="text.primary"
                            gutterBottom
                        >
                            My Advertisements
                        </Typography>
                    </Container>
                </Box>
                
                <Container maxWidth="md">
                    <Select
                        fullWidth
                        id='city'
                        name='city'
                        value={city || ''}
                        onChange={handleChange}
                        style={{ marginBottom: 20 + 'px' }}
                    >
                        {stateCities &&
                            stateCities.map((city, index) => {
                                return <MenuItem value={city} key={index}>{city}</MenuItem>
                            })
                        }
                    </Select>

                    {/* Valori statici per statistiche */}
                    <TableContainer component={Paper} style={{ marginBottom: 50 + 'px', maxHeight: "30rem", overflow: "auto" }}>
                        <Table sx={{ minWidth: 650 }} size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Jan</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Feb</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Mar</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Apr</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>May</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Jun</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Jul</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Aug</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Sep</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Oct</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Nov</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Dec</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>

                                <TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                    <TableCell align="center">1</TableCell>
                                    <TableCell align="center">4</TableCell>
                                    <TableCell align="center">21</TableCell>
                                    <TableCell align="center">3</TableCell>
                                    <TableCell align="center">33</TableCell>
                                    <TableCell align="center">98</TableCell>
                                    <TableCell align="center">5</TableCell>
                                    <TableCell align="center">17</TableCell>
                                    <TableCell align="center">7</TableCell>
                                    <TableCell align="center">86</TableCell>
                                    <TableCell align="center">23</TableCell>
                                    <TableCell align="center">69</TableCell>
                                </TableRow>
                            </TableBody>
                        </Table>
                    </TableContainer>

                </Container>

                <Container maxWidth="md">
                    <TableContainer component={Paper} style={{ marginBottom: 50 + 'px', maxHeight: "30rem", overflow: "auto" }}>
                        <Table sx={{ minWidth: 650 }} size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell align="left" style={{ fontWeight: 'bold' }}>Name</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Type</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>City</TableCell>
                                    <TableCell align="right" style={{ fontWeight: 'bold' }}>Price</TableCell>
                                    <TableCell align="right" style={{ fontWeight: 'bold' }}>Approved</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>

                                {accommodations.map((item) => (
                                    <TableRow key={item._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                        <TableCell align="left">
                                            <Link style={{ cursor: "pointer" }} onClick={() => { navigate("/accommodation/" + item._id) }}>
                                                {item.name}
                                            </Link>
                                        </TableCell>
                                        <TableCell align="center">Accommodation</TableCell>
                                        <TableCell align="center">{item.location.city}</TableCell>
                                        <TableCell align="right">{item.price}€</TableCell>
                                        <TableCell align="right">{item.approved ? "Approved" : "Not yet approved"}</TableCell>
                                    </TableRow>
                                ))}

                                {activities.map((item) => (
                                    <TableRow key={item._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                        <TableCell align="left">
                                            <Link style={{ cursor: "pointer" }} onClick={() => { navigate("/activity/" + item._id) }}>
                                                {item.name}
                                            </Link>
                                        </TableCell>
                                        <TableCell align="center">Activity</TableCell>
                                        <TableCell align="center">{item.location.city}</TableCell>
                                        <TableCell align="right">{item.price}€</TableCell>
                                        <TableCell align="right">{item.approved ? "Approved" : "Not yet approved"}</TableCell>
                                    </TableRow>
                                ))}

                            </TableBody>
                        </Table>
                    </TableContainer>
                </Container>
            </Container>

            <Box
                sx={{
                    py: 3,
                    px: 2,
                    mt: 'auto',
                }}
            />
        </ThemeProvider >
    );
}

export default MyAdv;