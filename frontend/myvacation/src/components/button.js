import {Link} from "react-router-dom";
import Button from '@mui/material/Button';
import * as React from 'react';

function CustomButton(){
    return (
      <div>
        <Button variant="contained">Contained</Button>
        <Link to="/login" >Go to login</Link>
      </div>
    );
}

export default CustomButton;