import * as React from 'react';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Modal from '@mui/material/Modal';
import Rating from '@mui/material/Rating';
import TextField from '@mui/material/TextField';
import api from "../utility/api";

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


const ReviewForm = ({destinationID}) => {
  const [open, setOpen] = React.useState(false);

  const handleOpen = async () => {

    await api.get("/review/check/"+destinationID).then(function(response){
      if(response.data.result === true){
        setOpen(true);
      } else{
        alert("Error: " +
            "you can review only a booked advertisement; " +
            "you can review only once");
      }
    })
    .catch(function(error){
      alert("Ops, something went wrong :(" + "\n" + error);
      return false;
    });
  }

  const handleClose = () => setOpen(false);

  const handleSubmit = (event) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const review = {
      "destinationType" : destinationType,
      "destinationID" : destinationID,
      "score" : data.get("rating"),
      "description" : data.get("description"),
      "reviewer" : localStorage.getItem("username")
    }

    api.put("/reviews" , review)
    .then(function(response){
      if(response.status === 200);
      setOpen(false);
      window.location.reload(false);
    })  
    .catch(function(error){
      alert("Ops, something went wrong :(" + "\n" + error);
    })
  }

  return (
    <div>
      {localStorage.getItem("userID") != null && localStorage.getItem("role") != "admin" ?
          <Button
              variant="outlined"
              style={{width:100+'%'}}
              onClick={handleOpen}
          >
            Leave a review
          </Button> : <></>
      }
      <Modal
        open={open}
        onClose={handleClose}
        aria-labelledby="modal-modal-title"
        aria-describedby="modal-modal-description"
      >
        <Box sx={style}>
            <form onSubmit={handleSubmit}>
          <Typography id="modal-modal-title" variant="h6" component="h2">
            Leave a review
          </Typography>
          <Rating name="rating" defaultValue={2.5} precision={0.5} />
          <TextField
                margin="normal"
                fullWidth
                name="description"
                label="Description"
                type="description"
                id="description"
                autoFocus
                />
            <Button variant="outlined" type = "submit" style={{width:100+'%'}} >Confirm</Button>
            </form>
        </Box>
      </Modal>
    </div>
  );
}

export default ReviewForm;