import * as React from 'react';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField'
import FileInput from "./inputFile";
import Container from '@mui/material/Container';

const AccommodationForm = ({ accommodation = null }) => {

    return (

        <Container maxWidth='md'>
            <FileInput fullWidth label="Images" />
            <TextField
                multiline
                InputLabelProps={{
                    shrink: accommodation ? true : undefined,
                }}
                defaultValue={accommodation ? accommodation.name : undefined}
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
                    shrink: accommodation ? true : undefined,
                }}
                defaultValue={accommodation ? accommodation.description : undefined}
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
                    shrink: accommodation ? true : undefined,
                }}
                defaultValue={accommodation ? accommodation.location.address : undefined}
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
                    shrink: accommodation ? true : undefined,
                }}
                defaultValue={accommodation ? accommodation.location.city : undefined}
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
                    shrink: accommodation ? true : undefined,
                }}
                defaultValue={accommodation ? accommodation.location.country : undefined}
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
                            shrink: accommodation ? true : undefined,
                        }}
                        defaultValue={accommodation ? accommodation.propertyType : undefined}
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
                        multiline
                        InputLabelProps={{
                            shrink: accommodation ? true : undefined,
                        }}
                        defaultValue={accommodation ? accommodation.guests : undefined}
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
                        multiline
                        InputLabelProps={{
                            shrink: accommodation ? true : undefined,
                        }}
                        defaultValue={accommodation ? accommodation.beds : undefined}
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
                            shrink: accommodation ? true : undefined,
                        }}
                        defaultValue={accommodation ? accommodation.price : undefined}
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
                            shrink: accommodation ? true : undefined,
                        }}
                        defaultValue={accommodation ? accommodation.bedrooms : undefined} 
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

export default AccommodationForm;