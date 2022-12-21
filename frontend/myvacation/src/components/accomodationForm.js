import * as React from 'react';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import FileInput from "./inputFile";
import Container from '@mui/material/Container';

const AccomodationForm = () => {

    return (

        <Container maxWidth='md'>
            <FileInput fullWidth label="Images" />

            <TextField
                margin="normal"
                required
                fullWidth
                name="name"
                label="Name"
                type="name"
                id="name"
                autoFocus
            />

            <TextField
                margin="normal"
                required
                fullWidth
                id="description"
                label="Description"
                name="description"
            />

            <TextField
                margin="normal"
                required
                fullWidth
                name="address"
                label="Address"
                id="address"
            />

            <TextField
                margin="normal"
                required
                fullWidth
                name="city"
                label="City"
                id="city"
            />
            <TextField
                margin="normal"
                required
                fullWidth
                name="country"
                label="Country"
                id="country"
            />


            <Grid container columnSpacing={2}>
                <Grid item xs={4} sm={4}>

                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="propertyType"
                        label="Tipo di proprietà"
                        id="propertyType"
                    />
                </Grid>
                <Grid item xs={4} sm={4}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="guests"
                        label="Guests number"
                        id="guests"
                        type="number"
                    />
                </Grid>
                <Grid item xs={4} sm={4}>

                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="beds"
                        label="Beds"
                        id="beds"
                        type="number"
                    />
                </Grid>
                <Grid item xs={4} sm={4}>

                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="price"
                        label="Price"
                        id="price"
                        type="number"
                    />
                </Grid>
                <Grid item xs={4} sm={4}>

                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="minimumNights"
                        label="Minimum nights"
                        id="minimumNights"
                        type="number"
                    />
                </Grid>
                <Grid item xs={4} sm={4}>

                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="bedrooms"
                        label="Bedrooms"
                        id="bedrooms"
                        type="number"
                    />
                </Grid>


            </Grid>
        </Container>



    );
};

export default AccomodationForm;