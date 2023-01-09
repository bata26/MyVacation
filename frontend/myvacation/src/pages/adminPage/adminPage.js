import * as React from 'react';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Container from '@mui/material/Container';
import ToBeApprovedList from './toBeApprovedList';
import UsersList from "./usersList";
import { Grid, TableContainer, Typography } from '@mui/material';
import TableCell from '@mui/material/TableCell';
import TableRow from '@mui/material/TableRow';
import Table from '@mui/material/Table';
import TableHead from '@mui/material/TableHead';
import Paper from '@mui/material/Paper';
import api from "../../utility/api";
import Config from "../../utility/config";

const theme = createTheme();

const AdminPage = () => {

	const [totalAdvertisement, setTotalAdvertisement] = React.useState([]);
	const [accommodationAverage, setAccommodationAverage] = React.useState([]);
	const [activityAverage, setActivityAverage] = React.useState([]);
	const [usersForMonth, setUsersForMonth] = React.useState([]);

	React.useEffect(() => {

		//Richiesta per avere il numero di annunci pubblicati (Accommodations/Activities)
		api.get("/analytics/totalAdvertisement")
			.then(function (response) {
				setTotalAdvertisement(response.data);
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});

		//Richiesta per avere la media dei prezzi per città delle accommodations
		api.get("/analytics/averageAccommodations")
			.then(function (response) {
				setAccommodationAverage(response.data);
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});

		//Richiesta per avere la media dei prezzi per città delle activities
		api.get("/analytics/averageActivities")
			.then(function (response) {
				setActivityAverage(response.data);
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});

		//Richiesta per avere il numero di iscritti in questo mese
		api.get("/analytics/usersForMonth")
			.then(function (response) {
				setUsersForMonth(response.data);
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
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
											<TableCell align="center" style={{ fontWeight: 'bold' }}>Accommodation</TableCell>
											<TableCell align="center" style={{ fontWeight: 'bold' }}>Activity</TableCell>
										</TableRow>
									</TableHead>
									<tbody>
										<TableRow sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
											<TableCell align="center">{totalAdvertisement.totalAccommodations}</TableCell>
											<TableCell align="center">{totalAdvertisement.totalActivities}</TableCell>
										</TableRow>
									</tbody>
								</Table>
							</TableContainer>
							}
						</Grid>
					</Grid>
					<Grid container columnSpacing={2}>
						{/* Tabella città - media prezzi ACCOMMODATIONS */}
						<Grid item xs={4} sm={6}>
							<Container maxWidth="sm">
								<Typography
									component="h3"
									variant="h5"
									align="center"
									color="text.primary"
									gutterBottom
								>
									Average Accommodations prices
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
										{accommodationAverage && accommodationAverage.map((accAv, index) => (
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
									Average Activities <br></br> prices
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
				</Container>
				<Container maxWidth="md" sx={{ mt: 4 }}>
					<Typography
						component="h2"
						variant="h4"
						align="center"
						color="text.primary"
						gutterBottom
					>
						Accommodations to be approved
					</Typography>
					{/* To be Approved List*/}
					<ToBeApprovedList destinationType={"accommodation"} />
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

