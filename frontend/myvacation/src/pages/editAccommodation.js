import * as React from 'react';
import Button from '@mui/material/Button';
import AccommodationForm from "../components/accommodationForm";
import FormData from 'form-data';
import api from '../utility/api';
import { useNavigate } from "react-router-dom";
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useParams } from 'react-router-dom';


async function convertFileToBase64(file) {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.readAsDataURL(file);
		reader.onload = () => resolve(reader.result);
		reader.onerror = reject;
	});
}

const EditAccommodation = () => {
	let navigate = useNavigate();
	const [accommodation, setAccommodation] = React.useState(null);
	const { accommodationID } = useParams();

	React.useEffect(() => {
		api.get('/accommodations/' + accommodationID)
			.then(function (response) {
				setAccommodation(response.data);
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});
	}, []);

	const handleSubmit = async (event) => {
		event.preventDefault();
		const data = new FormData(event.currentTarget);
		const result = await api.post('/edit/accommodations/' + accommodationID,
			data,
		)
			.then(function (response) {
				navigate("/accommodation/" + accommodationID);
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
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
							Edit accommodation
						</Typography>
					</Container>
				</Box>
				<AccommodationForm accommodation={accommodation} />
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

export default EditAccommodation;