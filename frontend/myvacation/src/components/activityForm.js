import * as React from 'react';
import Grid from '@mui/material/Unstable_Grid2';
import TextField from '@mui/material/TextField';
import FileInput from "./inputFile";
import Container from '@mui/material/Container';

const ActivityForm = () => {

    return (

        <Container maxWidth='md'>
            <FileInput fullWidth label="Images"/>

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
                <Grid item xs={4} sm={6}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        name="duration"
                        label="Duration (h)"
                        id="duration"
                        type="number"
                    />
                </Grid>
                <Grid item xs={4} sm={6}>

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
            </Grid>
        </Container>
    );
};

export default ActivityForm;