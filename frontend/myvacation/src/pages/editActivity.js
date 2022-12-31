import * as React from 'react';
import Button from '@mui/material/Button';
import FormData from 'form-data';
import api from '../utility/api';
import { useNavigate } from "react-router-dom";
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { useParams } from 'react-router-dom';
import ActivityForm from '../components/activityForm';


async function convertFileToBase64(file) {
	return new Promise((resolve, reject) => {
		const reader = new FileReader();
		reader.readAsDataURL(file);
		reader.onload = () => resolve(reader.result);
		reader.onerror = reject;
	});
}

const EditActivity = () => {
	let navigate = useNavigate();
	const [activity, setActivity] = React.useState(null);
	const { activityID } = useParams();

	React.useEffect(() => {
		api.get('/activities/' + activityID)
			.then(function (response) {
				setActivity(response.data);
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});
	}, []);

	const handleSubmit = async (event) => {
		event.preventDefault();
		const data = new FormData(event.currentTarget);
		const result = await api.post('/edit/activities/' + activityID,
			data,
		)
			.then(function (response) {
				navigate("/activity/" + activityID);
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
							Edit activity
						</Typography>
					</Container>
				</Box>
				<ActivityForm activity={activity} />
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

export default EditActivity;