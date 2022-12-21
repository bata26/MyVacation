import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { Box } from '@mui/system';
import { CssBaseline } from '@mui/material';
import Container from '@mui/system/Container';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';

const theme = createTheme();

export default function Home() {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />

            <Container maxWidth='lg'>

                <Box
                    sx={{
                        pt: 8,
                        pb: 6,
                    }}
                >
                    <Container maxWidth="sm">
                        <Typography
                            component="h2"
                            variant="h3"
                            align="center"
                            color="text.primary"
                            gutterBottom
                        >
                            Top cities of the month
                        </Typography>
                    </Container>
                </Box>

                <Grid container columnSpacing={2}>
                    <Grid item xs={4} sm={4}>
                        <Card sx={{ maxWidth: 345 }}>
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="div">
                                    #1 city of the month
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button size="small">Accomodations</Button>
                                <Button size="small">Activities</Button>
                            </CardActions>
                        </Card>
                    </Grid>

                    <Grid item xs={4} sm={4}>
                        <Card sx={{ maxWidth: 345 }}>
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="div">
                                    #2 city of the month
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button size="small">Accomodations</Button>
                                <Button size="small">Activities</Button>
                            </CardActions>
                        </Card>
                    </Grid>

                    <Grid item xs={4} sm={4}>
                        <Card sx={{ maxWidth: 345 }}>
                            <CardContent>
                                <Typography gutterBottom variant="h5" component="div">
                                    #3 city of the month
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button size="small">Accomodations</Button>
                                <Button size="small">Activities</Button>
                            </CardActions>
                        </Card>
                    </Grid>
                </Grid>

                <Box
                    sx={{
                        pt: 8,
                        pb: 6,
                    }}
                >
                    <Container maxWidth="sm">
                        <Typography
                            component="h2"
                            variant="h3"
                            align="center"
                            color="text.primary"
                            gutterBottom
                        >
                            Top 3 Accomodations
                        </Typography>
                    </Container>
                </Box>

                <Grid container spacing={4}>
                    <Grid item xs={12} sm={6} md={4}>
                        <Card
                            sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                        >
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Titolo
                                </Typography>
                            </CardContent>
                            <img src='https://picsum.photos/300/300' />
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography variant='span'>
                                    <b>City</b>
                                    <br />
                                    <i>Address</i>
                                    <br />
                                    Price€
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button fullWidth>View</Button>
                            </CardActions>
                        </Card>
                    </Grid>

                    <Grid item xs={12} sm={6} md={4}>
                        <Card
                            sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                        >
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Titolo
                                </Typography>
                            </CardContent>
                            <img src='https://picsum.photos/300/300' />
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography variant='span'>
                                    <b>City</b>
                                    <br />
                                    <i>Address</i>
                                    <br />
                                    Price€
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button fullWidth>View</Button>
                            </CardActions>
                        </Card>
                    </Grid>

                    <Grid item xs={12} sm={6} md={4}>
                        <Card
                            sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                        >
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Titolo
                                </Typography>
                            </CardContent>
                            <img src='https://picsum.photos/300/300' />
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography variant='span'>
                                    <b>City</b>
                                    <br />
                                    <i>Address</i>
                                    <br />
                                    Price€
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button fullWidth>View</Button>
                            </CardActions>
                        </Card>
                    </Grid>
                </Grid>

                <Box
                    sx={{
                        pt: 8,
                        pb: 6,
                    }}
                >
                    <Container maxWidth="sm">
                        <Typography
                            component="h2"
                            variant="h3"
                            align="center"
                            color="text.primary"
                            gutterBottom
                        >
                            Top 3 Activities
                        </Typography>
                    </Container>
                </Box>

                <Grid container spacing={4}>
                    <Grid item xs={12} sm={6} md={4}>
                        <Card
                            sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                        >
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Titolo
                                </Typography>
                            </CardContent>
                            <img src='https://picsum.photos/300/300' />
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography variant='span'>
                                    <b>City</b>
                                    <br />
                                    <i>Address</i>
                                    <br />
                                    Price€
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button fullWidth>View</Button>
                            </CardActions>
                        </Card>
                    </Grid>

                    <Grid item xs={12} sm={6} md={4}>
                        <Card
                            sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                        >
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Titolo
                                </Typography>
                            </CardContent>
                            <img src='https://picsum.photos/300/300' />
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography variant='span'>
                                    <b>City</b>
                                    <br />
                                    <i>Address</i>
                                    <br />
                                    Price€
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button fullWidth>View</Button>
                            </CardActions>
                        </Card>
                    </Grid>

                    <Grid item xs={12} sm={6} md={4}>
                        <Card
                            sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                        >
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography gutterBottom variant="h5" component="h2">
                                    Titolo
                                </Typography>
                            </CardContent>
                            <img src='https://picsum.photos/300/300' />
                            <CardContent sx={{ flexGrow: 1 }}>
                                <Typography variant='span'>
                                    <b>City</b>
                                    <br />
                                    <i>Address</i>
                                    <br />
                                    Price€
                                </Typography>
                            </CardContent>
                            <CardActions>
                                <Button fullWidth>View</Button>
                            </CardActions>
                        </Card>
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
            />
        </ThemeProvider>
    );
}