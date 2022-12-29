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
import api from "../../utility/api";

const theme = createTheme();

const AdminPage = () => {

	const [totalAdvertisement, setTotalAdvertisement] = React.useState([]);
	const [bestHostAcc, setBestHostAcc] = React.useState([]);
	const [bestHostAct, setBestHostAct] = React.useState([]);
	const [accomodationAverage, setAccomodationAverage] = React.useState([]);
	const [activityAverage, setActivityAverage] = React.useState([]);
	const [usersForMonth, setUsersForMonth] = React.useState([]);

	React.useEffect(() => {

		//Richiesta per avere il numero di annunci pubblicati (Accomodations/Activities)
		api.get("/analytics/totalAdvertisement")
			.then(function (response) {
				setTotalAdvertisement(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});

		//Richiesta per avere i top 10 host nel settore accomodation
		api.get("analytics/bestHost/accomodation")
			.then(function (response) {
				setBestHostAcc(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});

		//Richiesta per avere i top 10 host nel settore activity
		api.get("analytics/bestHost/activity")
			.then(function (response) {
				setBestHostAct(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});

		//Richiesta per avere la media dei prezzi per città delle accomodations
		api.get("/analytics/averageAccomodations")
			.then(function (response) {
				setAccomodationAverage(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});

		//Richiesta per avere la media dei prezzi per città delle activities
		api.get("/analytics/averageActivities")
			.then(function (response) {
				setActivityAverage(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});

		//Richiesta per avere il numero di iscritti in questo mese
		api.get("/analytics/usersForMonth")
			.then(function (response) {
				setUsersForMonth(response.data);
			})
			.catch(function (error) {
				console.log(error);
			});

	}, []);


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
					{/* Card iscrizioni mensili */}
					<Card sx={{ mb: 4 }}>
						<CardContent>
							<Typography gutterBottom variant="h5" component="div" align='center'>
								This month subscribed
							</Typography>
							<Typography gutterBottom variant="h5" component="div" align='center'>
								{usersForMonth.map((item) => (
									item.users
								))} users
							</Typography>
						</CardContent>
					</Card>

					{/* Card totale annunci */}
					<Card sx={{ mb: 4 }}>
						<CardContent>
							<Typography gutterBottom variant="h5" component="div" align='center'>
								Number of advertisements
							</Typography>
							<Typography gutterBottom variant="h5" component="div" align='center'>
								Accomodations: {totalAdvertisement.totalAccomodations}
							</Typography>
							<Typography gutterBottom variant="h5" component="div" align='center'>
								Activities: {totalAdvertisement.totalActivities}
							</Typography>
						</CardContent>
					</Card>

					<Grid container columnSpacing={2}>
						<Container maxWidth="sm">
							<Typography
								component="h3"
								variant="h5"
								align="center"
								color="text.primary"
								gutterBottom
							>
								Average pricies Accomodation/Activity
							</Typography>
						</Container>
						{/* Tabella città - media prezzi ACCOMODATIONS */}
						<Grid item xs={4} sm={6}>
							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
								<Table sx={{ minWidth: 650 }} size="small">
									<TableHead>
										<TableRow>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>City</TableCell>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>Average cost</TableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{accomodationAverage.map((accAv) => (
											<TableRow key={accAv._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
												<TableCell align="center">{accAv.city} </TableCell>
												<TableCell align="center">{accAv.averageCost}</TableCell>
											</TableRow>
										))}
									</TableBody>
								</Table>
							</TableContainer>
						</Grid>

						{/* Tabella città - media prezzi ACTIVITIES */}
						<Grid item xs={4} sm={6}>
							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
								<Table size="small">
									<TableHead>
										<TableRow>
											<TableCell align="left" style={{ fontWeight: 'bold' }}>City</TableCell>
											<TableCell align="left" style={{ fontWeight: 'bold' }}>Average cost</TableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{activityAverage.map((actAv) => (
											<TableRow key={actAv._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
												<TableCell align="center">{actAv.city} </TableCell>
												<TableCell align="center">{actAv.averageCost}</TableCell>
											</TableRow>
										))}
									</TableBody>
								</Table>
							</TableContainer>
						</Grid>
					</Grid>

					<Grid container columnSpacing={2}>
						<Container maxWidth="sm">
							<Typography
								component="h3"
								variant="h5"
								align="center"
								color="text.primary"
								gutterBottom
							>
								Top 10 hosts Accomodation/Activity
							</Typography>
						</Container>

						{/* Tabella top 10 host accomodations */}
						<Grid item xs={4} sm={6}>
							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
								<Table sx={{ minWidth: 650 }} size="small">
									<TableHead>
										<TableRow>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>HostID</TableCell>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>Average Rating</TableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{bestHostAcc.map((hostAcc) => (
											<TableRow key={hostAcc._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
												<TableCell align="center">{hostAcc.hostID} </TableCell>
												<TableCell align="center">{hostAcc.averageRating}</TableCell>
											</TableRow>
										))}
									</TableBody>
								</Table>
							</TableContainer>
						</Grid>

						{/* Tabella top 10 host activities */}
						<Grid item xs={4} sm={6}>
							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
								<Table sx={{ minWidth: 650 }} size="small">
									<TableHead>
										<TableRow>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>HostID</TableCell>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>Average Rating</TableCell>
										</TableRow>
									</TableHead>
									<TableBody>
										{bestHostAct.map((hostAct) => (
											<TableRow key={hostAct._id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
												<TableCell align="center">{hostAct.hostID} </TableCell>
												<TableCell align="center">{hostAct.averageRating}</TableCell>
											</TableRow>
										))}
									</TableBody>
								</Table>
							</TableContainer>
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
					<ToBeApprovedList destinationType={"accomodation"} />
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
					<ToBeApprovedList destinationType={"activity"} />
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

