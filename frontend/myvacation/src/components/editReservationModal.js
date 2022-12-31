import React  from "react";
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import TextField from '@mui/material/TextField';
import api from "../utility/api";
import EditIcon from "@mui/icons-material/Edit";
import { useNavigate } from "react-router-dom";
import Moment from 'moment';





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


const EditReservationModal = ({reservation}) => {
    const [open, setOpen] = React.useState(false);
    const [startDate, setStartDate] = React.useState(reservation.startDate);
    const [endDate, setEndDate] = React.useState(reservation.endDate);
    const today = new Date();
    const date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
    const navigate = useNavigate();

    const handleOpen = () => setOpen(true);

    const handleClose = () => setOpen(false);

    const onChangeStartDate = (event) => {
        setStartDate(event.target.value);
    }

    const onChangeEndDate = (event) => {
        setEndDate(event.target.value);
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        let updatedData;
        if(reservation.destinationType === "accomodation") {
            updatedData = {
                "startDate": data.get("startDate"),
                "endDate": data.get("endDate"),
                "reservation" : reservation
            }
        }
        else {
            updatedData = {
                "startDate": data.get("startDate"),
                "reservation" : reservation
            }
        }

        api.patch("/reservation/" + reservation._id , updatedData)
            .then(function(response){
                alert("Reservation updated correctly");
                setOpen(false);
                window.location.reload(true);
            })
            .catch(function(error){
                alert("Already booked for this period/date");
            })
    }

    return (
        <div>
            <EditIcon color="primary" style={{ cursor: "pointer" }} onClick={handleOpen}/>
            <Modal
                open={open}
                onClose={handleClose}
                aria-labelledby="modal-modal-title"
                aria-describedby="modal-modal-description"
            >
                <Box sx={style}>
                    <form onSubmit={handleSubmit}>
                        <Typography id="modal-modal-title" variant="h6" component="h2">
                            Update your Reservation
                        </Typography>
                        <TextField
                            fullWidth
                            id="startDate"
                            name="startDate"
                            type="text"
                            required={true}
                            onFocus={(e) => (e.target.type = "date")}
                            onBlur={(e) => (e.target.type = "text")}
                            placeholder={Moment(reservation.startDate).utc().format('MMM DD YYYY')}
                            onChange={onChangeStartDate}
                            InputProps={{ inputProps: { min:`${date}`, max:""} }}
                            style={{width:100+'%', marginTop:10}}
                        />
                    {reservation.destinationType === "accomodation" ?
                        (<TextField
                            fullWidth
                            id="endDate"
                            name="endDate"
                            type="text"
                            required={true}
                            onChange={onChangeEndDate}
                            onFocus={(e) => (e.target.type = "date")}
                            onBlur={(e) => (e.target.type = "text")}
                            placeholder={Moment(endDate).utc().format('MMM DD YYYY')}
                            InputProps={{ inputProps: { min:`${startDate}`, max:""}, }}
                            style={{width:100+'%', marginTop:10}}
                        />) : <></>}
                        <Button variant="outlined" type = "submit" style={{width:100+'%', marginTop:10}} >Update</Button>
                    </form>
                </Box>
            </Modal>
        </div>
    );
}

export default EditReservationModal;