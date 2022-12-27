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

                {/* Tabella città - media prezzi */}

                {/* Tabella top 10 host */}

                {/* Card totale annunci */}

                {/* Andamento iscrizioni */}


                <Container maxWidth="md" sx={{ mt: 4 }}>
                    <Typography
                        component="h2"
                        variant="h4"
                        align="center"
                        color="text.primary"
                        gutterBottom
                    >
                        To be approved
                    </Typography>
                    {/* To be Approved List*/}
                    <ToBeApprovedList />
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

