import * as React from 'react';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField'
import FileInput from "./inputFile";
import Container from '@mui/material/Container';

const AccomodationForm = ({ accomodation = null }) => {

    return (

        <Container maxWidth='md'>
            <FileInput fullWidth label="Images" />
            <TextField
                multiline
                InputLabelProps={{
                    shrink: accomodation ? true : false,
                }}
                defaultValue={accomodation ? accomodation.name : undefined}
                margin="normal"
                required
                fullWidth
                id="name"
                label="Name"
                name="name"
                autoFocus
            />

            <TextField
                multiline
                InputLabelProps={{
                    shrink: accomodation ? true : false,
                }}
                defaultValue={accomodation ? accomodation.description : undefined}
                margin="normal"
                required
                fullWidth
                id="description"
                label="Description"
                name="description"
            />

            <TextField
                multiline
                InputLabelProps={{
                    shrink: accomodation ? true : false,
                }}
                defaultValue={accomodation ? accomodation.location.address : undefined}
                margin="normal"
                required
                fullWidth
                name="address"
                label="Address"
                id="address"
            />

            <TextField
                multiline
                InputLabelProps={{
                    shrink: accomodation ? true : false,
                }}
                defaultValue={accomodation ? accomodation.location.city : undefined}
                margin="normal"
                required
                fullWidth
                name="city"
                label="City"
                id="city"
            />
            <TextField
                multiline
                InputLabelProps={{
                    shrink: accomodation ? true : false,
                }}
                defaultValue={accomodation ? accomodation.location.country : undefined}
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
                        multiline
                        InputLabelProps={{
                            shrink: accomodation ? true : false,
                        }}
                        defaultValue={accomodation ? accomodation.property_type : undefined}
                        margin="normal"
                        required
                        fullWidth
                        name="property_type"
                        label="Tipo di proprietà"
                        id="property_type"
                    />
                </Grid>
                <Grid item xs={4} sm={4}>
                    <TextField
                        multiline
                        InputLabelProps={{
                            shrink: accomodation ? true : false,
                        }}
                        defaultValue={accomodation ? accomodation.accommodates : undefined}
                        margin="normal"
                        required
                        fullWidth
                        name="accommodates"
                        label="Guests number"
                        id="accommodates"
                        type="number"
                    />
                </Grid>
                <Grid item xs={4} sm={4}>

                    <TextField
                        multiline
                        InputLabelProps={{
                            shrink: accomodation ? true : false,
                        }}
                        defaultValue={accomodation ? accomodation.beds : undefined}
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
                        multiline
                        InputLabelProps={{
                            shrink: accomodation ? true : false,
                        }}
                        defaultValue={accomodation ? accomodation.price : undefined}
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
                        multiline
                        InputLabelProps={{
                            shrink: accomodation ? true : false,
                        }}
                        defaultValue={accomodation ? accomodation.minimum_nights : undefined}
                        margin="normal"
                        required
                        fullWidth
                        name="minimum_nights"
                        label="Minimum nights"
                        id="minimum_nights"
                        type="number"
                    />
                </Grid>
                <Grid item xs={4} sm={4}>
                    <TextField
                        multiline
                        InputLabelProps={{
                            shrink: accomodation ? true : false,
                        }}
                        defaultValue={accomodation ? accomodation.bedrooms : undefined} 
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