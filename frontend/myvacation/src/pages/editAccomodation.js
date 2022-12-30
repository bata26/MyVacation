import * as React from 'react';
import Button from '@mui/material/Button';
import AccomodationForm from "../components/accomodationForm";
import FormData from 'form-data';
import api from '../utility/api';
import { useNavigate } from "react-router-dom";
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useParams, useSearchParams } from 'react-router-dom';


async function convertFileToBase64(file) {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.readAsDataURL(file);
		reader.onload = () => resolve(reader.result);
		reader.onerror = reject;
	});
}

const EditAccomodation = () => {
	let navigate = useNavigate();
	const [accomodation, setAccomodation] = React.useState(null);
	const { accomodationID } = useParams();

	React.useEffect(() => {
		api.get('/accomodations/' + accomodationID)
			.then(function (response) {
				console.log(response.data);
				setAccomodation(response.data);
			})
			.catch(function (error) {
				console.log("errore");
			});
	}, []);

	const handleSubmit = async (event) => {
		event.preventDefault();
		const data = new FormData(event.currentTarget);
		//const formData = new FormData();
		//console.log("form: ", data.get("bedrooms"));
		//const headers = { 'Content-type': 'multipart/form-data' };
		const result = await api.post('/edit/accomodations/' + accomodationID,
			data,
		)
			.then(function (response) {
				console.log(response.data);
				navigate("/accomodation/" + accomodationID);
			})
			.catch(function (error) {
				console.log("errore");
			});
	};

	return (
		<form onSubmit={handleSubmit}>
			<Container component="main" maxWidth="lg">
				<CssBaseline />
				<Box
					sx={{
						pt: 8,
						pb: 6,
					}}
				>
					<Container maxWidth="lg">
						<Typography
							component="h1"
							variant="h2"
							align="center"
							color="text.primary"
							gutterBottom
						>
							Edit accomodation
						</Typography>
					</Container>
				</Box>
				<AccomodationForm accomodation={accomodation} />
				<Container maxWidth='md'>
					<Button
						type="submit"
						fullWidth
						variant="contained"
						sx={{ mt: 2 }}
					>
						Modify
					</Button>
				</Container>
			</Container>
			<Box
				sx={{
					py: 3,
					px: 2,
					mt: 'auto',
				}}
			>
			</Box>
		</form>
	);
};

export default EditAccomodation;