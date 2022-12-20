import * as React from 'react';
import CssBaseline from '@mui/material/CssBaseline';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Card from '@mui/material/Card';
import CardActions from '@mui/material/CardActions';
import CardContent from '@mui/material/CardContent';
import CardMedia from '@mui/material/CardMedia';
import CardActionArea from '@mui/material/CardActionArea';
import Button from "@mui/material/Button";
import { useSearchParams } from "react-router-dom";
import api from "../api/api";
import moment from "moment";
import { useNavigate } from 'react-router-dom';
import { Box } from '@mui/system';



const theme = createTheme();

export default function Checkout() {
    const [searchParams] = useSearchParams();
    const startDate = searchParams.get("startDate");
    const endDate = searchParams.get("endDate");
    const reservedId = searchParams.get("id")
    const type = searchParams.get("type")
    const guests = searchParams.get("guests")
    const [reserved, setReserved] = React.useState(null);
    const [totalExpense, setTotalExpense] = React.useState(null);
    const navigate = useNavigate();

    React.useEffect(() => {
        api.get("/" + type + "/" + reservedId)
            .then(function (response) {
                setReserved(response.data);
                console.log(response.data);
                console.log(startDate);
                console.log(endDate);
                if (type === "accomodations") {
                    const timeStart = moment(startDate);
                    const timeEnd = moment(endDate);
                    const diff = timeEnd.diff(timeStart);
                    const diffDuration = moment.duration(diff);
                    setTotalExpense(response.data.price * diffDuration.days())
                }
                else if (type === "activities")
                    //setTotalExpense(response.data.price * guests)
                    setTotalExpense(response.data.price)
            })
            .catch(function (error) {
                console.log(error);
            });
    }, []);

    //Setter per la url di visualizzazione oggetto
    let setter = "";

    if (type === "accomodations") {
        setter = "accomodation"
    } else {
        setter = "activity"
    }

    async function reserve(reservation) {
        console.log(reservation);
        console.log(startDate);
        console.log(endDate);
        if (type === "accomodations") {
            const bodyRequest = {
                "accomodation": reservation,
                "startDate": startDate,
                "endDate": endDate,
            };
            await api.post("/book/accomodation", bodyRequest)
                .then(function (response) {
                    alert("Prenotazione avvenuta con successo!")
                    navigate("/", { replace: true });
                })
                .catch(function (error) {
                    console.log("error : ", error);
                    alert("Impossibile prenotare, riprova più tardi");
                });
        }
        else if (type === "activities") {
            console.log(reservation);
            console.log(startDate);

            const bodyRequest = {
                "activity": reservation,
                "startDate": startDate
            };
            await api.post("/book/activity", bodyRequest)
                .then(function (response) {
                    alert("Prenotazione avvenuta con successo!")
                    navigate("/", { replace: true });
                })
                .catch(function (error) {
                    console.log("error : ", error);
                    alert("Impossibile prenotare, riprova più tardi");
                })
        }
    }

    return (
        <ThemeProvider theme={theme}>
            <Container component="main" maxWidth="xl">
                <CssBaseline />
                <Box>
                    <Box
                        sx={{
                            pt: 8,
                            pb: 6,
                        }}
                    >
                        <Container maxWidth="xl">
                            <Typography
                                component="h1"
                                variant="h2"
                                align="center"
                                color="text.primary"
                                gutterBottom
                            >
                                Checkout
                            </Typography>
                        </Container>
                    </Box>
                </Box>
            </Container>

            {reserved && (
            <Container maxWidth="sm">
                <Card>
                    <CardActionArea onClick={() => {navigate("/" + setter + "/" + reservedId + "?startDate=" + startDate + "&endDate=" + endDate + "&guests=" + guests)}}>
                        <CardMedia
                            component="img"
                            height="140"
                            width="340"
                            image={`data:image/jpeg;base64,${reserved.mainPicture}`}
                            alt="Main Picture"
                        />
                        <CardContent>
                            <Typography gutterBottom variant="h5" component="div">
                                {reserved.name} - {reserved.host_name}
                            </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    <b>{startDate} - {endDate}</b>
                                    <br/>
                                    <b>{reserved.location.city}</b>
                                    <br/>
                                    {reserved.location.address}
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    <b>{"€" + totalExpense}</b>
                                </Typography>
                        </CardContent>
                    </CardActionArea>
                    
                    <CardActions>
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                            onClick={()=> {reserve(reserved)}}
                        >
                            Confirm
                        </Button>
                    </CardActions>
                </Card>
            </Container>)}

            <Box
                component="footer"
                sx={{
                    py: 3,
                    px: 2,
                    mt: 'auto',
                }}
            >
            </Box>
        </ThemeProvider>
    );
}