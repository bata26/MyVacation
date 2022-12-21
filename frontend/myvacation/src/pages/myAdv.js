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


const theme = createTheme();

const MyAdv = () => {

    const profileID = localStorage.getItem("userID");
    const navigate = useNavigate();

    let [accomodations, setAccomodations] = React.useState([]);
    let [activities, setActivities] = React.useState([]);

    React.useEffect( () =>{
        //Richiesta per recuperare le accomodations dell'utente
        api.get("/myadvacc/" + profileID)
        .then(function (response) {
            setAccomodations(response.data);
        })
        .catch(function (error) {
            console.log(error);
            }
        );

        //Richiesta per recuperare le activities dell'utente
        api.get("/myadvact/" + profileID)
        .then(function (response) {
            setActivities(response.data);
        })
        .catch(function (error) {
            console.log(error);
            }
        );
    } , []);

    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="md">
                <CssBaseline/>

                <Box sx={{pt: 8, pb: 6}}>
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
                    <TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
                        <Table sx={{ minWidth: 650 }} size="small">
                            <TableHead>
                                <TableRow>
                                    <TableCell align="left" style={{ fontWeight: 'bold' }}>Name</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>Type</TableCell>
                                    <TableCell align="center" style={{ fontWeight: 'bold' }}>City</TableCell>
                                    <TableCell align="right" style={{ fontWeight: 'bold' }}>Price</TableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>

                                {accomodations.map((item) => (
                                <TableRow key={item._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                    <TableCell align="left">
                                        <Link style={{ cursor: "pointer" }} onClick={() => {navigate("/accomodation/" + item._id)}}>
                                            {item.name}
                                        </Link>
                                    </TableCell>                                    
                                    <TableCell align="center">Accomodation</TableCell>
                                    <TableCell align="center">{item.location.city}</TableCell>
                                    <TableCell align="right">{item.price}€</TableCell>
                                </TableRow>
                                ))}

                                {activities.map((item) => (
                                <TableRow key={item._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                    <TableCell align="left">
                                        <Link style={{ cursor: "pointer" }} onClick={() => {navigate("/activity/" + item._id)}}>
                                            {item.name}
                                        </Link>
                                    </TableCell>
                                    <TableCell align="center">Activity</TableCell>
                                    <TableCell align="center">{item.location.city}</TableCell>
                                    <TableCell align="right">{item.price}€</TableCell>
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
        </ThemeProvider>
    );
    }

export default MyAdv;