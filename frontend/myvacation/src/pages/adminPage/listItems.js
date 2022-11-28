import * as React from 'react';
import ListItemButton from '@mui/material/ListItemButton';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import ListSubheader from '@mui/material/ListSubheader';
import DashboardIcon from '@mui/icons-material/Dashboard';
import ShoppingCartIcon from '@mui/icons-material/ShoppingCart';
import PeopleIcon from '@mui/icons-material/People';
import BarChartIcon from '@mui/icons-material/BarChart';
import LayersIcon from '@mui/icons-material/Layers';
import AssignmentIcon from '@mui/icons-material/Assignment';
import {useNavigate} from "react-router-dom";



function MainListItems() {
    let navigate = useNavigate();

    const changePage = (pagePath) => {
        console.log("sono dentro -> path : ", pagePath);
        navigate(pagePath);
    };

    return (
    <React.Fragment>
        <ListItemButton onClick={() => {changePage("/admin")}}>
            <ListItemIcon>
                <DashboardIcon/>
            </ListItemIcon>
            <ListItemText primary="Dashboard"/>
        </ListItemButton>
        <ListItemButton onClick={() => {changePage("/reports")}}>
            <ListItemIcon>
                <BarChartIcon/>
            </ListItemIcon>
            <ListItemText primary="Reports"/>
        </ListItemButton>
    </React.Fragment>)
}

export default MainListItems;