import * as React from 'react';
import Grid from '@mui/material/Unstable_Grid2';
import TextField from '@mui/material/TextField';
import FileInput from "./inputFile";
import Container from '@mui/material/Container';

const ActivityForm = ({ activity = null }) => {

    return (

        <Container maxWidth='md'>
            <FileInput fullWidth label="Images" />

            <TextField
                multiline
                InputLabelProps={{
                    shrink: activity ? true : false,
                }}
                defaultValue={activity ? activity.name : undefined}
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
                multiline
                InputLabelProps={{
                    shrink: activity ? true : false,
                }}
                defaultValue={activity ? activity.description : undefined}
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
                    shrink: activity ? true : false,
                }}
                defaultValue={activity ? activity.location.address : undefined}
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
                    shrink: activity ? true : false,
                }}
                defaultValue={activity ? activity.location.city : undefined}
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
                    shrink: activity ? true : false,
                }}
                defaultValue={activity ? activity.location.country : undefined}
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
                        multiline
                        InputLabelProps={{
                            shrink: activity ? true : false,
                        }}
                        defaultValue={activity ? activity.duration : undefined}
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
                        multiline
                        InputLabelProps={{
                            shrink: activity ? true : false,
                        }}
                        defaultValue={activity ? activity.price : undefined}
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