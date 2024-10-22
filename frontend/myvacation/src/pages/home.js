import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { Box } from '@mui/system';
import { CssBaseline } from '@mui/material';
import Container from '@mui/system/Container';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import PersonIcon from '@mui/icons-material/Person';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import api from '../utility/api';
import { useNavigate } from 'react-router-dom';

const theme = createTheme();

const Home = () => {
	const [accommodations, setAccommodations] = React.useState([]);
	const [activities, setActivities] = React.useState([]);
	const [cities, setCities] = React.useState([]);
	const [recommendedUsers, setRecommendedUsers] = React.useState([]);
	const [recommendedAccommodations, setRecommendedAccommodations] = React.useState([]);
	const [recommendedActivities, setRecommendedActivities] = React.useState([]);
	const navigate = useNavigate();

	React.useEffect(() => {
		async function getHomeData() {
			let request = {};
			await api.get("/analytics/topcities")
				.then(function (response) {
					setCities(response.data);
				})
				.catch(function (error) {
					alert("Ops, something went wrong :(" + "\n" + error);
				})

			await api.get("/analytics/topadv")
				.then(async function (response) {
					const requestBody = response.data;
					request = {
						"accommodationsID": [],
						"activitiesID": []
					};
					requestBody.accommodationsID.map(accommodationID => request.accommodationsID.push(accommodationID._id));
					requestBody.activitiesID.map(activityID => request.activitiesID.push(activityID._id));

					await api.post("/analytics/advinfo", JSON.stringify(request))
						.then(function (response) {
							setAccommodations(response.data["accommodations"]);
							setActivities(response.data["activities"]);
						})
						.catch(function (error) {
							alert("Ops, something went wrong :(" + "\n" + error);
						})
				})
				.catch(function (error) {
					alert("Ops, something went wrong :(" + "\n" + error);
				})

			if (localStorage.getItem("userID") !== null && localStorage.getItem("userID") !== undefined && localStorage.getItem("role") !== "admin") {
				await api.get("/recommendations/user")
					.then(function (response) {
						setRecommendedUsers(response.data);
					})
					.catch(function (error) {
						alert("Ops, something went wrong :(" + "\n" + error);
					})

				await api.get("/recommendations/accommodation")
					.then(function (response) {
						setRecommendedAccommodations(response.data);
					})
					.catch(function (error) {
						alert("Ops, something went wrong :(" + "\n" + error);
					})

				await api.get("/recommendations/activity")
					.then(function (response) {
						setRecommendedActivities(response.data);
					})
					.catch(function (error) {
						alert("Ops, something went wrong :(" + "\n" + error);
					})
			}

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
							<Grid item xs={4} sm={4} key={index}>
								<Card sx={{ maxWidth: 345 }}>
									<CardContent>
										<Typography gutterBottom variant="h5" component="div">
											#{index + 1} {item.city}
										</Typography>
									</CardContent>
									<CardActions>
										<Button size="small"
												onClick={() => {navigate("/search?city=" + item.city + "&type=accommodations")}}
												variant="contained"
												color='info'
										>
											Accommodations
										</Button>
										<Button
											size="small"
											onClick={() => {navigate("/search?city=" + item.city + "&type=activities")}}
											variant="contained"
											color='info'
										>
											Activities
										</Button>
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
							Top 3 Accommodations
						</Typography>
					</Container>
				</Box>

				<Grid container spacing={4}>
					{
						accommodations.map((item, index) => (
							<Grid item xs={12} sm={6} md={4} key={index}>
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
											<i>{item.location.address}</i>
											<br />
											{item.price}€
										</Typography>
									</CardContent>
									<CardActions>
										<Button fullWidth
												onClick={() => navigate("/accommodation/" + item._id)}
												variant="contained"
												color='info'
										>
											View
										</Button>
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
							<Grid item xs={12} sm={6} md={4} key={index}>
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
											<i>{item.location.address}</i>
											<br />
											{item.price}€
										</Typography>
									</CardContent>
									<CardActions>
										<Button
											fullWidth
											onClick={() => navigate("/activity/" + item._id)}
											variant="contained"
											color='info'
										>
											View
										</Button>
									</CardActions>
								</Card>
							</Grid>
						))
					}
				</Grid>
				{localStorage.getItem("role") !== "admin" && localStorage.getItem("userID") != null ?
				<>
				{/* Profili suggeriti */}
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
							Recommended Users
						</Typography>
					</Container>
				</Box>
				<Grid container spacing={4}>
					{recommendedUsers && recommendedUsers.map((item, index) => (
						<Grid item xs={12} sm={6} md={4} key={index}>
							<Card
								sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
							>
								<CardContent sx={{ flexGrow: 1 }}>
									<Typography gutterBottom variant="h5" component="h2">
										{item.username}
									</Typography>
									<PersonIcon />
								</CardContent>
								<CardActions>
									<Button
										fullWidth
										onClick={() => navigate("/profile/" + item.userID)}
										variant="contained"
										color='info'
									>
										View
									</Button>
								</CardActions>
							</Card>
						</Grid>
					))
					}
				</Grid>
				{/*Alloggi suggeriti */}
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
							Recommended Accommodations
						</Typography>
					</Container>
				</Box>

				<Grid container spacing={4}>
					{recommendedAccommodations && recommendedAccommodations.map((item, index) => (
						<Grid item xs={12} sm={6} md={4} key={index}>
							<Card
								sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
							>
								<CardContent sx={{ flexGrow: 1 }}>
									<Typography gutterBottom variant="h5" component="h2">
										{item.name}
									</Typography>
								</CardContent>
								<CardActions>
									<Button
										fullWidth
										onClick={() => navigate("/accommodation/" + item.accommodationID)}
										variant="contained"
										color='info'
									>
										View
									</Button>
								</CardActions>
							</Card>
						</Grid>
					))
					}
				</Grid>
				{/* Attività suggerite */}
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
							Recommended Activities
						</Typography>
					</Container>
				</Box>
				<Grid container spacing={4}>
					{recommendedActivities && recommendedActivities.map((item, index) => (
						<Grid item xs={12} sm={6} md={4} key={index}>
							<Card
								sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}
							>
								<CardContent sx={{ flexGrow: 1 }}>
									<Typography gutterBottom variant="h5" component="h2">
										{item.name}
									</Typography>
								</CardContent>
								<CardActions>
									<Button
										fullWidth
										onClick={() => navigate("/activity/" + item.activityID)}
										variant="contained"
										color='info'
									>
										View
									</Button>
								</CardActions>
							</Card>
						</Grid>
					))
					}
				</Grid>
				</> : <></>
				}
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