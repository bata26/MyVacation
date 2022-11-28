import * as React from 'react';
import Grid from '@mui/material/Unstable_Grid2';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import FormControlLabel from '@mui/material/FormControlLabel';
import { FormControl } from '@mui/material';
import FormLabel from '@mui/material/FormLabel';
import FileInput from "./inputFile";
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';

const AccomodationForm = () => {

    return(
        <Grid container spacing={2}>
            {/** ROW 1 */}
            <Grid xs={3}/>
            <Grid xs = {6}>
                <FileInput label="Immagini" />

                <TextField
                margin="normal"
                required
                fullWidth
                name="name"
                label="Nome"
                type="name"
                id="name"
                autoFocus
                />

                <TextField
                margin="normal"
                required
                fullWidth
                id="description"
                label="Descrizione"
                name="description"
                />
                
                <TextField
                margin="normal"
                required
                fullWidth
                name="address"
                label="Indirizzo"
                id="address"
                />

                <TextField
                margin="normal"
                required
                fullWidth
                name="city"
                label="Città"
                id="city"
                />
                <TextField
                margin="normal"
                required
                fullWidth
                name="country"
                label="Nazione"
                id="country"
                />
                <TextField
                margin="normal"
                required
                fullWidth
                name="propertyType"
                label="Tipo di proprietà"
                id="propertyType"
                />
            </Grid>
            <Grid xs={3} />
            {/** ROW 2 */}
            <Grid xs={3} />

            <Grid xs = {3}>
                <TextField
                margin="normal"
                required
                fullWidth
                name="guests"
                label="Numero di ospiti"
                id="guests"
                type="number"
                />
            </Grid>
            <Grid xs = {3}>
                <TextField
                margin="normal"
                required
                fullWidth
                name="beds"
                label="Numero letti"
                id="beds"
                type="number"
                />
            </Grid>
            <Grid xs = {3}/>
            {/** GROW 3 */}
            <Grid xs = {3}/>
            <Grid xs = {3}>
                <TextField
                margin="normal"
                required
                fullWidth
                name="price"
                label="Prezzo"
                id="price"
                type="number"
                />
            </Grid>
            <Grid xs = {3}>
                <TextField
                margin="normal"
                required
                fullWidth
                name="minimumNights"
                label="Notti minime"
                id="minimumNights"
                type="number"
                />
            </Grid>
        </Grid>
    );
};

export default AccomodationForm;