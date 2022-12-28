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
import api from '../utility/api';
import { useNavigate } from 'react-router-dom';

const theme = createTheme();

const Home = () => {
    const [accomodations, setAccomodations] = React.useState([]);
    const [activities, setActivities] = React.useState([]);
    const [cities, setCities] = React.useState([]);
    const navigate = useNavigate();

    React.useEffect(() => {
        async function getHomeData() {
            let request = {};
            await api.get("/analytics/topcities")
                .then(function (response) {
                    setCities(response.data);
                })
                .catch(function (error) {
                    console.log(error);
                })

            await api.get("/analytics/topadv")
                .then(async function (response) {
                    const requestBody = response.data;
                    request = {
                        "accomodationsID": [],
                        "activitiesID": []
                    };
                    console.log(requestBody);
                    requestBody.accomodationsID.map(accomodationID => request.accomodationsID.push(accomodationID._id));
                    requestBody.activitiesID.map(activityID => request.activitiesID.push(activityID._id));
                    console.log(request);
                    await api.post("/analytics/advinfo", JSON.stringify(request))
                        .then(function (response) {
                            setAccomodations(response.data["accomodations"]);
                            setActivities(response.data["activities"]);
                        })
                        .catch(function (error) {
                            console.log(error);
                        })
                })
                .catch(function (error) {
                    console.log(error);
                })
        }
        getHomeData();
    }, []);

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
                    {
                        cities.map((item, index) => (
                            <Grid item xs={4} sm={4}>
                                <Card sx={{ maxWidth: 345 }}>
                                    <CardContent>
                                        <Typography gutterBottom variant="h5" component="div">
                                            #{index + 1} {item.city}
                                        </Typography>
                                    </CardContent>
                                    <CardActions>
                                        <Button size="small" onClick={() => {
                                            navigate("/search?city=" + item.city)
                                        }}>Accomodations</Button>
                                        <Button size="small" onClick={() => {
                                            navigate("/search?city=" + item.city)
                                        }}>Activities</Button>
                                    </CardActions>
                                </Card>
                            </Grid>
                        ))
                    }
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
                    {
                        accomodations.map((item, index) => (
                            <Grid item xs={12} sm={6} md={4}>
                                <Card
                                    sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                                >
                                    <CardContent sx={{ flexGrow: 1 }}>
                                        <Typography gutterBottom variant="h5" component="h2">
                                            {item.name}
                                        </Typography>
                                    </CardContent>
                                    <img
                                        src={`data:image/jpeg;base64,${item.mainPicture}`}
                                    />
                                    <CardContent sx={{ flexGrow: 1 }}>
                                        <Typography variant='span'>
                                            <b>{item.location.city}</b>
                                            <br />
                                            <i>{item.location.city}</i>
                                            <br />
                                            {item.price}€
                                        </Typography>
                                    </CardContent>
                                    <CardActions>
                                        <Button fullWidth>View</Button>
                                    </CardActions>
                                </Card>
                            </Grid>
                        ))
                    }
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
                {
                        activities.map((item, index) => (
                            <Grid item xs={12} sm={6} md={4}>
                                <Card
                                    sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
                                >
                                    <CardContent sx={{ flexGrow: 1 }}>
                                        <Typography gutterBottom variant="h5" component="h2">
                                            {item.name}
                                        </Typography>
                                    </CardContent>
                                    <img
                                        src={`data:image/jpeg;base64,${item.mainPicture}`}
                                    />
                                    <CardContent sx={{ flexGrow: 1 }}>
                                        <Typography variant='span'>
                                            <b>{item.location.city}</b>
                                            <br />
                                            <i>{item.location.city}</i>
                                            <br />
                                            {item.price}€
                                        </Typography>
                                    </CardContent>
                                    <CardActions>
                                        <Button fullWidth>View</Button>
                                    </CardActions>
                                </Card>
                            </Grid>
                        ))
                    }                                       
                </Grid>

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
};

export default Home;