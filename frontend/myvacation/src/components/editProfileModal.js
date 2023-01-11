import React from "react";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';
import api from "../utility/api";
import Moment from 'moment';
import Grid from "@mui/material/Grid";
import { FormControl } from "@mui/material";
import FormLabel from "@mui/material/FormLabel";
import RadioGroup from "@mui/material/RadioGroup";
import FormControlLabel from "@mui/material/FormControlLabel";
import Radio from "@mui/material/Radio";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import Config from "../utility/config";
import MenuItem from "@mui/material/MenuItem";


const style = {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: 400,
    bgcolor: 'background.paper',
    border: '2px solid #000',
    boxShadow: 24,
    p: 4,
};


const EditProfileModal = ({ id, name, surname, gender, dateOfBirth, nationalityProp, knownLanguages }) => {
    const [open, setOpen] = React.useState(false);
    const [languages, setLanguages] = React.useState([]);
    const [nationality, setNationality] = React.useState(nationalityProp);
    const today = new Date();
    const date = (today.getFullYear() - 16) + '-' + (today.getMonth() + 1) + '-' + today.getDate();

    const handleOpen = () => {
        setOpen(true)
    }

    const handleChangeLanguages = (event) => {
        const {
            target: { value },
        } = event;
        setLanguages(value);
    }


    const handleNationalityChange = (event) => {
        setNationality(event.target.value);
    };

    const handleClose = () => setOpen(false);


    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);

        const updatedData = {
            "name": data.get("name"),
            "surname": data.get("surname"),
            "dateOfBirth": data.get("dateOfBirth"),
            "nationality": nationality,
            "knownLanguages": languages,
            "gender": data.get("gender")
        }
        console.log(updatedData);
        api.patch("/user/" + id, updatedData)
            .then(function (response) {
                alert("Profile updated correctly");
                setOpen(false);
                window.location.reload(true);
            })
            .catch(function (error) {
                alert("Ops, something went wrong :(" + "\n" + error);
            })
    }

    return (
        <div>
            <Button color="info" variant="contained" fullWidth onClick={handleOpen} sx={{ mt: 2 }}>Update Profile</Button>
            <Modal
                open={open}
                onClose={handleClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box component="form" onSubmit={handleSubmit} noValidate sx={style}>
                    <Typography id="modal-modal-title" variant="h6" component="h2" sx={{ mb: 2 }}>
                        Update your Profile
                    </Typography>
                    <Grid container columnSpacing={1.4}>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                //autoComplete="given-name"
                                name="name"
                                required
                                fullWidth
                                id="name"
                                label="Name"
                                autoFocus
                                defaultValue={name}
                            />
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <TextField
                                required
                                fullWidth
                                id="surname"
                                label="Surname"
                                name="surname"
                                defaultValue={surname}
                            />
                        </Grid>
                    </Grid>
                    <FormControl>
                        <FormLabel id="gender" margin='normal'>Gender</FormLabel>
                        <RadioGroup
                            aria-labelledby="gender"
                            defaultValue={gender}
                            name="gender"
                            row
                        >
                            <FormControlLabel value="male" control={<Radio />} label="Male" />
                            <FormControlLabel value="female" control={<Radio />} label="Female" />
                            <FormControlLabel value="other" control={<Radio />} label="Other" />
                        </RadioGroup>
                    </FormControl>
                    <TextField
                        fullWidth
                        id="dateOfBirth"
                        name="dateOfBirth"
                        type="text"
                        onFocus={(e) => (e.target.type = "date")}
                        onBlur={(e) => (e.target.type = "text")}
                        placeholder={Moment(dateOfBirth).utc().format('MMM DD YYYY')}
                        style={{ width: 100 + '%', marginTop: 10 }}
                        InputProps={{ inputProps: { min: "", max: `${date}` } }}
                    />
                    <InputLabel id="demo-simple-select-label">Nationality</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="nationality"
                        label="Nationality"
                        onChange={handleNationalityChange}
                        fullWidth
                        required
                        value={nationality}
                    >
                        {Config.NATIONALITY_LIST.map((item, index) => {
                            return <MenuItem value={item} key={index}>{item}</MenuItem>
                        })}
                    </Select>
                    <InputLabel id="demo-simple-select-label">Languages</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="knownLanguages"
                        name="knownLanguages"
                        label="Languages"
                        multiple
                        value={languages}
                        onChange={handleChangeLanguages}
                        fullWidth
                        required
                    >
                        {Config.LANGUAGE_LIST.map((item, index) => {
                            return <MenuItem key={index} value={item}>{item}</MenuItem>
                        })}
                    </Select>
                    <Button variant="contained" type="submit" style={{ width: 100 + '%', marginTop: 10 }} >Update</Button>
                    <Button variant="contained" color="error" style={{ width: 100 + '%', marginTop: 10 }} onClick={() => { window.location.reload(true) }} >Cancel</Button>
                    <Grid container>
                        <Grid item xs>
                        </Grid>
                        <Grid item>
                        </Grid>
                    </Grid>
                </Box>
            </Modal>
        </div>
    );
}

export default EditProfileModal;