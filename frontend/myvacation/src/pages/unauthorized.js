import { useNavigate } from "react-router-dom"
import Button from '@mui/material/Button';
import { Typography } from '@mui/material';
import Grid from '@mui/material/Unstable_Grid2';


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
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
};

const Unauthorized = () => {
    const navigate = useNavigate();

    const goBack = () => navigate(-1);

    const goToSignIn = () => navigate("/signin");

    return (

            <Grid sx={style}>
                <Typography variant="h6" component="h1">Unauthorized</Typography>
                <Typography>You do not have access to the requested page.</Typography>
                {localStorage.getItem("userID") == null ?
                    <Button
                        variant="contained"
                        color='info'
                        onClick={goToSignIn}
                        align="center"
                    >
                        Sign In
                    </Button> : <></>
                }
                <Button
                    variant="contained"
                    color='error'
                    onClick={goBack}
                    align="center"
                    sx={{mt: 2}}
                >
                    Go Back
                </Button>
            </Grid>
    )
}

export default Unauthorized