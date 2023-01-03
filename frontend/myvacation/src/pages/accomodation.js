import * as React from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import Grid from '@mui/material/Unstable_Grid2';
import ImageList from '@mui/material/ImageList';
import ImageListItem from '@mui/material/ImageListItem';
import ReactHtmlParser from 'react-html-parser';
import api from "../utility/api";
import Button from '@mui/material/Button';
import ReviewForm from '../components/reviewForm';
import { CardActions, Typography } from '@mui/material';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Container from '@mui/material/Container';
import CssBaseline from '@mui/material/CssBaseline';
import Box from '@mui/material/Box';
import { useNavigate } from "react-router-dom";
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import ThumbUpAltIcon from '@mui/icons-material/ThumbUpAlt';
import ThumbUpOffAltIcon from '@mui/icons-material/ThumbUpOffAlt';


const theme = createTheme();

const Accomodation = () => {
	const [accomodation, setAccomodation] = React.useState(null);
	const [reviews, setReviews] = React.useState(null);
	const [totLikes, setTotLikes] = React.useState(null);
	const [enableButton, setEnableButton] = React.useState(null);
	const [likedAdv, setLikedAdv] = React.useState(null);
	const [searchParams] = useSearchParams();
	const { accomodationID } = useParams();
	const [startDate, setStartDate] = React.useState(searchParams.get("startDate") === "" ? null : searchParams.get("startDate"))
	const [endDate, setEndDate] = React.useState(searchParams.get("endDate") === "" ? null : searchParams.get("endDate"))
	const [guests, setGuests] = React.useState(searchParams.get("guests") === "" ? null : searchParams.get("guests"))
	const navigate = useNavigate();

	function getTotalLikes() {
		api.get('/likenumber/accomodation/' + accomodationID)
			.then(function (response) {
				setTotLikes(response.data.likes)
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});
	}

	React.useEffect(() => {
		api.get("/accomodations/" + accomodationID)
			.then(function (response) {
				setAccomodation(response.data);
				setReviews(response.data.reviews)
				if (response.data.reviews.length >= parseInt(process.env.REACT_APP_REVIEWS_SIZE))
					setEnableButton(true)
				else
					setEnableButton(false)
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});

		api.get('/users/liking/accomodation/' + accomodationID)
			.then(function (response) {
				setLikedAdv(response.data.liked)
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});
		getTotalLikes();

	}, []);


	//Metodo per eliminare accomodation
	const deleteAccomodation = (accomodationID) => {
		api.delete("/accomodations/" + accomodationID)
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});
		navigate('/search')
	}

	//Metodo per eliminare review
	const deleteReview = async (reviewID) => {
		await api.delete("/reviews/accomodation/" + accomodationID + "/" + reviewID)
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});
		window.location.reload(false);
	}


	if (!accomodation) return null;

	function goToCheckout() {
		navigate("/checkout?startDate=" + startDate + "&endDate=" + endDate + "&type=accomodations" + "&id=" + accomodation._id + "&guests=" + guests)
	}

	const getAllReviews = async () => {
		await api.get("/reviewsByDestination/" + accomodationID)
			.then(function (response) {
				setReviews(response.data);
				setEnableButton(false);
			})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});
	}


	const likeAdv = async (likedAdvID, likedAdvName) => {
		await api.post("/users/liking", {
			"likedAdvID": likedAdvID,
			"likedAdvName": likedAdvName,
			"destinationType": "accomodation"
		}).then(function (response) {
			console.log(response.data);
			setLikedAdv(true);
			getTotalLikes();
		})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});
	}

	const unlikeAdv = async (unlikedAdvID, unlikedAdvName) => {
		await api.post("/users/unliking", {
			"unlikedAdvID": unlikedAdvID,
			"unlikedAdvName": unlikedAdvName,
			"destinationType": "accomodation"
		}).then(function (response) {
			console.log(response.data);
			setLikedAdv(false);
			getTotalLikes();
		})
			.catch(function (error) {
				alert("Ops, something went wrong :(" + "\n" + error);
			});
	}

	return (
		((accomodation && accomodation.approved) || (accomodation && !accomodation.approved && localStorage.getItem("userID") === accomodation.host_id) || localStorage.getItem("role") === "admin") ?
			(<ThemeProvider theme={theme}>
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
									{accomodation.name}
								</Typography>
							</Container>
						</Box>
					</Box>
				</Container>

				{/* Immagini */}
				<Container maxWidth='lg'>
					<ImageList
						sx={{ width: 100 + '%', height: 99 + '%' }}
						variant="quilted"
						gap={5}
						cols={3}
						rowHeight={200}
					>
						<ImageListItem key={accomodation.mainPicture} cols={2} rows={3}>
							<img
								src={`data:image/jpeg;base64,${accomodation.mainPicture}`}
								style={{ borderRadius: 10 + 'px' }}
							/>
						</ImageListItem>
						{accomodation.pictures.map((item) => (
							<ImageListItem key={item}>
								<img
									src={`data:image/jpeg;base64,${item}`}
									style={{ borderRadius: 10 + 'px' }}
								/>
							</ImageListItem>
						))}
					</ImageList>
				</Container>
				<Container maxWidth='lg'>
					<Grid alignItems={"left"}>
						{localStorage.getItem("userID") != null && accomodation.approved ?
							(!likedAdv ?
								<Button onClick={() => { likeAdv(accomodation._id, accomodation.name) }}>
									<ThumbUpOffAltIcon
										variant="filled"
										sx={{ fontSize: 40 }}
									/>
								</Button>
								:
								<Button onClick={() => { unlikeAdv(accomodation._id, accomodation.name) }}>
									<ThumbUpAltIcon
										variant="filled"
										sx={{ fontSize: 40 }}
									/>
								</Button>
							) : <></>
						}
						<Typography>
							<b>{totLikes}</b>
						</Typography>
					</Grid>
				</Container>
				<Container maxWidth='lg'>
					<Grid container spacing={24}>
						<Grid item xs={6}>
							<Typography
								component="h2"
								variant="h4"
								align="left"
								color="text.primary"
								gutterBottom
								sx={{ mt: 2 }}
							>
								Description
							</Typography>

							<Typography
								component="h2"
								variant="h6"
								align="left"
								color="text.primary"
							>
								{ReactHtmlParser(accomodation.description)}
							</Typography>
						</Grid>

						<Grid item xs={6}>
							<Typography
								component="h3"
								variant="h4"
								align="right"
								color="text.primary"
								gutterBottom
							>
								Price
							</Typography>

							<Typography
								align='right'
								component="h3"
								variant="h5"
								color="text.primary"
								sx={{ mb: 2 }}
							>
								{accomodation.price}€
							</Typography>

							<Typography
								component="h3"
								variant="h4"
								align="right"
								color="text.primary"
								gutterBottom
							>
								Other information
							</Typography>

							<Typography align='right' sx={{ mb: 2 }}>
								<b>Host:</b> {accomodation.host_name}
								<br />
								<b>Beds:</b> {accomodation.beds}
								<br />
								<b>Minimum nights:</b> {accomodation.minimum_nights}
								<br />
								<b>Guests:</b> {accomodation.accommodates}
								<br />
								<b>Bedrooms:</b> {accomodation.bedrooms}
								<br />
								<b>Address:</b> {accomodation.location.address}
								<br />
								<b>Country:</b> {accomodation.location.country}
								<br />
								<b>City:</b> {accomodation.location.city}
								<br />
								{startDate ?
									<>
										<b>Start date:</b> {startDate}
									</> : <></>
								}
								{endDate ?
									<>
										<br />
										<b>End date:</b> {endDate}
									</> : <></>
								}
							</Typography>
							{startDate != null && endDate != null && localStorage.getItem("userID") != null && accomodation.approved ?
								<Button
									fullWidth
									variant="contained"
									color="success"
									sx={{ mb: 2 }}
									onClick={() => goToCheckout()}>
									Book Accomodation
								</Button> : <></>}
							{accomodation.approved ? <ReviewForm destinationID={accomodation._id} destinationType={"accomodation"} /> : <></>}
							{
								accomodation.approved && (localStorage.getItem("userID") === accomodation.host_id || localStorage.getItem("role") === "admin") ?
									(<>
										<Button
											fullWidth
											variant="contained"
											color='error'
											sx={{ mt: 2 }}
											onClick={() => {
												deleteAccomodation(accomodation._id)
											}}
										>
											Delete Accomodation
										</Button>
										<Button
											fullWidth
											variant="contained"
											color='info'
											sx={{ mt: 2 }}
											onClick={() => {
												navigate("/update/accomodation/" + accomodationID)
											}}
										>
											Update Accomodation
										</Button>
									</>
									)
									: <></>
							}
						</Grid>
					</Grid>
				</Container>

				<Box
					sx={{
						py: 3,
						px: 2,
						mt: 'auto',
					}}
				>
				</Box>
				{accomodation.approved ? (
					<Container maxWidth='lg'>
						<Typography
							component="h2"
							variant="h4"
							align="center"
							color="text.primary"
							gutterBottom
							sx={{ mt: 2 }}
						>
							Reviews
						</Typography>
						<Grid
							sx={{ overflowY: "scroll", maxHeight: "1460px" }}
						>
							{reviews && reviews.map((item) => (
								<Card key={item._id} sx={{ maxHeight: 180, marginTop: 2 }}>
									<CardContent>
										<Typography gutterBottom variant="h5" component="div">
											{item.reviewer} - {item.score}
										</Typography>
										<Typography variant="body2" color="text.secondary">
											{item.description}
										</Typography>
									</CardContent>
									<CardActions>
										{localStorage.getItem("userID") && (localStorage.getItem("userID") === item.userID || localStorage.getItem("role") === "admin") ?
											<Button color='error' onClick={() => { deleteReview(item._id) }}>
												Delete
											</Button> : <></>
										}
										{localStorage.getItem("userID") ?
											<Button color='info' onClick={() => navigate("/profile/" + item.userID)}>
												View Profile
											</Button> : <></>
										}
									</CardActions>
								</Card>
							))}
						</Grid>
						{enableButton ?
							<Container maxWidth='sm'>
								<Button
									fullWidth
									variant="contained"
									sx={{ mt: 2 }}
									onClick={() => getAllReviews()}
								>
									More reviews
								</Button>
							</Container> : <></>}
					</Container>) : <></>}
				<Box
					sx={{
						py: 3,
						px: 2,
						mt: 'auto',
					}}
				>
				</Box>
			</ThemeProvider>) : alert("You don't have the right permission")
	);
};

export default Accomodation;