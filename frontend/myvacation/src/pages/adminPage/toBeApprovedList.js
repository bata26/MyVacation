import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './title';
import api from "../../api/api";
import TableContainer from "@mui/material/TableContainer";
import Paper from "@mui/material/Paper";
import TableFooter from "@mui/material/TableFooter";
import {useNavigate} from "react-router-dom";
import Button from "@mui/material/Button";
import useAuth from '../../hooks/useAuth';


export default function ToBeApprovedList() {
    const [last_id, setLast_id] = React.useState(null);
    const [first_id, setFirst_id] = React.useState(null);
    const [page, setPage] = React.useState(1);
    const [toBeApprovedList, setToBeApprovedList] = React.useState(null);
    const navigate = useNavigate();
    const {auth} = useAuth();

    React.useEffect(() => {
        api.get("/admin/announcements?index=" , {headers:{"Authorization":JSON.stringify(auth)}})
            .then(function (response) {
                setToBeApprovedList(response.data);
                setLast_id(response.data[response.data.length -1]._id);
                setFirst_id(response.data[0]._id);
                console.log(response);
                console.log(response.data);
            })
            .catch(function (error) {
                console.log(error);
            });
    }, []);

    const handlePreviousPage = () => {
        setPage(page-1)
        const url ="?index=" + first_id + "&direction=previous";
        console.log(url);
        api.get("/admin/announcements"+url)
            .then(function (response) {
                setToBeApprovedList(response.data);
                if (response && response.data.length > 0 ) {
                    setLast_id(response.data[0]._id);
                    setFirst_id(response.data[response.data.length - 1]._id);
                }
                console.log(response.data);
                console.log(first_id)
                console.log(last_id)
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    const handleNextPage = () => {
        setPage(page+1);
        const url = "?index=" + last_id + "&direction=next";
        console.log(url);
        api.get("/admin/announcements"+url)
            .then(function (response) {
                setToBeApprovedList(response.data);
                if (response && response.data.length > 0 ) {
                    setLast_id(response.data[response.data.length - 1]._id);
                    setFirst_id(response.data[0]._id);
                }
                else{
                    setFirst_id(last_id)
                }
                console.log(response.data);
                console.log(first_id)
                console.log(last_id)
            })
            .catch(function (error) {
                console.log(error);
            });

    };

    const handleFirstPage = () => {
        setPage(1);
        const url ="?index=";

        console.log(url);
        api.get("/admin/announcements"+url)
            .then(function (response) {
                setToBeApprovedList(response.data);
                setLast_id(response.data[4]._id);
                console.log(response.data);
            })
            .catch(function (error) {
                console.log(error);
                console.log(first_id)
                console.log(last_id)
            });
    };

    const emptyRows =
        page > 1 ? Math.max(0, 2 - toBeApprovedList ? toBeApprovedList.length : 0) : 0;

    return (

        <TableContainer component={Paper}>
            <Title>To be approved list</Title>
            <Table sx={{ minWidth: 500 }} aria-label="custom pagination table">
                <TableHead>
                    <TableRow>
                        <TableCell>HostId</TableCell>
                        <TableCell>Title</TableCell>
                        <TableCell>City</TableCell>
                        <TableCell>Type</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    { toBeApprovedList && toBeApprovedList.map((row) => (
                        <TableRow key={row._id} onClick={()=>{navigate("/" + row.type + "/" + row._id)}} selected={true}>
                            <TableCell component="th" scope="row">
                                {row.host_id}
                            </TableCell>
                            <TableCell component="th" scope="row">
                                {row.name}
                            </TableCell>
                            <TableCell style={{ width: 160 }} align="right">
                                {row.location.city}
                            </TableCell>
                            <TableCell style={{ width: 160 }} align="right">
                                {row.type}
                            </TableCell>
                        </TableRow>
                    ))}
                    {emptyRows > 0 && (
                        <TableRow style={{ height: 53 * emptyRows }}>
                            <TableCell colSpan={6} />
                        </TableRow>
                    )}
                </TableBody>
                <TableFooter>
                    <TableRow>
                        <TableCell>
                            {page !== 1 ? <Button onClick={() => {handlePreviousPage()}}>Previous</Button> : <></>}
                            {toBeApprovedList && toBeApprovedList.length === 2 ? <Button onClick={() => {handleNextPage()}}>Next</Button> : <></>}
                            {page !== 1 ? <Button onClick={() => {handleFirstPage()}}> First</Button> : <></>}
                        </TableCell>
                    </TableRow>
                </TableFooter>
            </Table>
        </TableContainer>
    );
}