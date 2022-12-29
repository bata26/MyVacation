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
import Config from "../../utility/config";

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
					<Grid container columnSpacing={2}>
						<Grid item xs={4} sm={6}>

							{/* Card iscrizioni mensili */}
							<Container maxWidth="sm">
								<Typography
									component="h3"
									variant="h5"
									align="center"
									color="text.primary"
									gutterBottom
								>
									User subscription per month
								</Typography>
							</Container>

							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
								<Table size="small">
									<TableHead>
										<TableRow>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>Month</TableCell>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>User</TableCell>
										</TableRow>
									</TableHead>
									<tbody>
										{usersForMonth && usersForMonth.map((item, index) => (
											<TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
												<TableCell align="center">{Config.MONTHS[item.month-1]}</TableCell>
												<TableCell align="center">{item.users}</TableCell>
											</TableRow>
										))}
									</tbody>
								</Table>
							</TableContainer>
						</Grid>

						<Grid item xs={4} sm={6}>
							{/* Card totale annunci */}
							<Container maxWidth="sm">
								<Typography
									component="h3"
									variant="h5"
									align="center"
									color="text.primary"
									gutterBottom
								>
									Number of advertisements
								</Typography>
							</Container>
							{totalAdvertisement &&
							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
								<Table size="small">
									<TableHead>
										<TableRow>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>Accomodation</TableCell>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>Activity</TableCell>
										</TableRow>
									</TableHead>
									<tbody>
										<TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
											<TableCell align="center">{totalAdvertisement.totalAccomodations}</TableCell>
											<TableCell align="center">{totalAdvertisement.totalActivities}</TableCell>
										</TableRow>
									</tbody>
								</Table>
							</TableContainer>
							}
						</Grid>
					</Grid>

					<Grid container columnSpacing={2}>
						{/* Tabella città - media prezzi ACCOMODATIONS */}
						<Grid item xs={4} sm={6}>
							<Container maxWidth="sm">
								<Typography
									component="h3"
									variant="h5"
									align="center"
									color="text.primary"
									gutterBottom
								>
									Average Accomodations's prices
								</Typography>
							</Container>
							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px', maxHeight: "30rem", overflow: "auto" }} >
								<Table size="small">
									<TableHead>
										<TableRow>
											<TableCell align="left" style={{ fontWeight: 'bold' }}>City</TableCell>
											<TableCell align="right" style={{ fontWeight: 'bold' }}>Average cost</TableCell>
										</TableRow>
									</TableHead>
									<tbody>
										{accomodationAverage && accomodationAverage.map((accAv, index) => (
											<TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
												<TableCell align="left">{accAv.city} </TableCell>
												<TableCell align="right">{accAv.averageCost}</TableCell>
											</TableRow>
										))}
									</tbody>
								</Table>
							</TableContainer>
						</Grid>

						{/* Tabella città - media prezzi ACTIVITIES */}
						<Grid item xs={4} sm={6}>
							<Container maxWidth="sm">
								<Typography
									component="h3"
									variant="h5"
									align="center"
									color="text.primary"
									gutterBottom
								>
									Average Activities's prices
								</Typography>
							</Container>
							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px', maxHeight: "30rem", overflow: "auto" }} >
								<Table size="small">
									<TableHead>
										<TableRow>
											<TableCell align="left" style={{ fontWeight: 'bold' }}>City</TableCell>
											<TableCell align="right" style={{ fontWeight: 'bold' }}>Average cost</TableCell>
										</TableRow>
									</TableHead>
									<tbody>
										{activityAverage && activityAverage.map((actAv, index) => (
											<TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
												<TableCell align="left">{actAv.city} </TableCell>
												<TableCell align="right">{actAv.averageCost}</TableCell>
											</TableRow>
										))}
									</tbody>
								</Table>
							</TableContainer>
						</Grid>
					</Grid>

					<Grid container columnSpacing={2}>


						{/* Tabella top 10 host accomodations */}
						<Grid item xs={4} sm={6}>
							<Container maxWidth="sm">
								<Typography
									component="h4"
									variant="h5"
									align="center"
									color="text.primary"
									gutterBottom
								>
									Top 10 Accomodation's hosts
								</Typography>
							</Container>
							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
								<Table size="small">
									<TableHead>
										<TableRow>
											<TableCell align="left" style={{ fontWeight: 'bold' }}>HostID</TableCell>
											<TableCell align="right" style={{ fontWeight: 'bold' }}>Average Rating</TableCell>
										</TableRow>
									</TableHead>
									<tbody>
										{bestHostAcc && bestHostAcc.map((hostAcc, index) => (
											<TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
												<TableCell align="left">{hostAcc.hostID} </TableCell>
												<TableCell align="right">{hostAcc.averageRating}</TableCell>
											</TableRow>
										))}
									</tbody>
								</Table>
							</TableContainer>
						</Grid>

						{/* Tabella top 10 host activities */}
						<Grid item xs={4} sm={6}>
							<Container maxWidth="sm">
								<Typography
									component="h4"
									variant="h5"
									align="center"
									color="text.primary"
									gutterBottom
								>
									Top 10 Activity's hosts
								</Typography>
							</Container>
							<TableContainer component={Paper} style={{ marginBottom: 50 + 'px' }} >
								<Table size="small">
									<TableHead>
										<TableRow>
											<TableCell align="left" style={{ fontWeight: 'bold' }}>HostID</TableCell>
											<TableCell align="right" style={{ fontWeight: 'bold' }}>Average Rating</TableCell>
										</TableRow>
									</TableHead>
									<tbody>
										{bestHostAct && bestHostAct.map((hostAct, index) => (
											<TableRow key={index} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
												<TableCell align="left">{hostAct.hostID} </TableCell>
												<TableCell align="right">{hostAct.averageRating}</TableCell>
											</TableRow>
										))}
									</tbody>
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

