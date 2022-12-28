import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import ToBeApprovedList from './toBeApprovedList';
import UsersList from "./usersList";
import { Grid, TableContainer, Typography } from '@mui/material';
import TableCell from '@mui/material/TableCell';
import TableBody from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Paper from '@mui/material/Paper';

const theme = createTheme();

const AdminPage = () => {

    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="md">
                <CssBaseline />
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
                            Admin Page
                        </Typography>
                    </Container>
                </Box>



                <Container maxWidth="sm">
                    <Typography
                        component="h2"
                        variant="h4"
                        align="center"
                        color="text.primary"
                        gutterBottom
                    >
                        Analytics
                    </Typography>
                </Container>



                <Container maxWidth="md" sx={{ mt: 4 }}>

                    {/* Grafico andamento iscrizioni */}
                    <Card sx={{ mb: 4 }}>
                        <CardContent>
                            <Typography gutterBottom variant="h5" component="div" align='center'>
                                This month subscribed
                            </Typography>
                            <Typography gutterBottom variant="h5" component="div" align='center'>
                                10 users
                            </Typography>
                        </CardContent>
                    </Card>

                    <Grid container columnSpacing={1.4}>

                        {/* Tabella città - media prezzi */}
                        <Grid item xs={4} sm={2.7}>
                            <TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
                                <Table size="small">
                                    <TableHead>
                                        <TableRow>
                                            <TableCell align="center" style={{ fontWeight: 'bold' }}>Average price per city</TableCell>

                                        </TableRow>
                                    </TableHead>
                                    <TableBody>

                                        <TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                            <TableCell align="center">Roma </TableCell>
                                            <TableCell align="center">350€</TableCell>

                                        </TableRow>

                                        <TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                            <TableCell align="center">Milano</TableCell>
                                            <TableCell align="center">650€</TableCell>

                                        </TableRow>

                                        <TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                            <TableCell align="center">Torino</TableCell>
                                            <TableCell align="center">450€</TableCell>

                                        </TableRow>

                                    </TableBody>
                                </Table>
                            </TableContainer>
                        </Grid>

                        <Grid item xs={4} sm={2.7}>
                            {/* Tabella top 10 host */}
                            <TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
                                <Table size="small">
                                    <TableHead>
                                        <TableRow>
                                            <TableCell align="center" style={{ fontWeight: 'bold' }}>Top 10 hosts</TableCell>

                                        </TableRow>
                                    </TableHead>
                                    <TableBody>

                                        <TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                            <TableCell align="center">Luca </TableCell>
                                            <TableCell align="center">Rossi</TableCell>

                                        </TableRow>

                                        <TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                            <TableCell align="center">Matteo</TableCell>
                                            <TableCell align="center">Verdi</TableCell>

                                        </TableRow>

                                        <TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                                            <TableCell align="center">Mario</TableCell>
                                            <TableCell align="center">Grossi</TableCell>

                                        </TableRow>

                                    </TableBody>
                                </Table>
                            </TableContainer>


                        </Grid>

                        {/* Card totale annunci */}
                        <Grid item xs={4} sm={3.2}>
                            <Card>
                                <CardContent>
                                    <Typography gutterBottom variant="h5" component="div" align='center'>
                                        Number of advertisements
                                    </Typography>
                                    <Typography gutterBottom variant="h5" component="div" align='center'>
                                        500
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                        {/* Card totale utenti */}
                        <Grid item xs={4} sm={3.2}>
                            <Card>
                                <CardContent>
                                    <Typography gutterBottom variant="h5" component="div" align='center'>
                                        Number of users
                                    </Typography>
                                    <Typography gutterBottom variant="h5" component="div" align='center'>
                                        100
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                    </Grid>
                </Container>


                <Container maxWidth="md" sx={{ mt: 4 }}>
                    <Typography
                        component="h2"
                        variant="h4"
                        align="center"
                        color="text.primary"
                        gutterBottom
                    >
                        Accomodations to be approved
                    </Typography>
                    {/* To be Approved List*/}
                    <ToBeApprovedList destinationType={"accomodation"}/>
                    <Typography
                        component="h2"
                        variant="h4"
                        align="center"
                        color="text.primary"
                        gutterBottom
                        sx={{ mt: 4 }}
                    >
                        Activities to be approved
                    </Typography>
                    <ToBeApprovedList destinationType={"activity"}/>
                </Container>

                <Container maxWidth="md" sx={{ mt: 4 }}>
                    <Typography
                        component="h2"
                        variant="h4"
                        align="center"
                        color="text.primary"
                        gutterBottom
                    >
                        Users
                    </Typography>
                    {/* Users List */}
                    <UsersList />
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

export default AdminPage;

