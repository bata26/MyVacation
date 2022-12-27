import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import api from "../../utility/api";
import TableContainer from "@mui/material/TableContainer";
import Paper from "@mui/material/Paper";
import { useNavigate } from "react-router-dom";
import Button from "@mui/material/Button";
import { Container } from '@mui/system';
import { Grid } from '@mui/material';


export default function ToBeApprovedList() {
    const [last_id, setLast_id] = React.useState(null);
    const [first_id, setFirst_id] = React.useState(null);
    const [page, setPage] = React.useState(1);
    const [toBeApprovedList, setToBeApprovedList] = React.useState(null);
    const navigate = useNavigate();
    const [lastPage, setLastPage] = React.useState(null);


    React.useEffect(() => {
        api.get("/admin/announcements?index=")
            .then(function (response) {
                setToBeApprovedList(response.data);
                if (response.data.length !== 0) {
                    setLast_id(response.data[response.data.length - 1]._id);
                    setFirst_id(response.data[0]._id);
                    if (response.data.length === parseInt(process.env.REACT_APP_ADMIN_PAGE_SIZE))
                        setLastPage(false)
                }
            })
            .catch(function (error) {
                console.log(error);
            });
    }, []);

    const handlePreviousPage = () => {
        setPage(page - 1)
        const url = "?index=" + first_id + "&direction=previous";
        console.log(url);
        api.get("/admin/announcements" + url)
            .then(function (response) {
                setToBeApprovedList(response.data);
                if (response && response.data.length > 0) {
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
        setPage(page + 1);
        const url = "?index=" + last_id + "&direction=next";
        console.log(url);
        api.get("/admin/announcements" + url)
            .then(function (response) {
                setToBeApprovedList(response.data);
                if (response && response.data.length > 0) {
                    setLast_id(response.data[response.data.length - 1]._id);
                    setFirst_id(response.data[0]._id);
                }
                else {
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
        const url = "?index=";

        console.log(url);
        api.get("/admin/announcements" + url)
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
            <Table sx={{ minWidth: 500 }} size='small'>
                <TableHead>
                    <TableRow>
                        <TableCell align="left" style={{ fontWeight: 'bold' }}>HostID</TableCell>
                        <TableCell align="center" style={{ fontWeight: 'bold' }}>Title</TableCell>
                        <TableCell align="center" style={{ fontWeight: 'bold' }}>City</TableCell>
                        <TableCell align="right" style={{ fontWeight: 'bold' }}>Type</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {toBeApprovedList && toBeApprovedList.map((row) => (
                        <TableRow key={row._id} onClick={() => { navigate("/toApprove/" + row._id + "?type=" + row.type) }} style={{ cursor: "pointer" }}>
                            <TableCell align='left' component="th" scope="row">
                                {row.host_id}
                            </TableCell>
                            <TableCell align='center' component="th" scope="row">
                                {row.name}
                            </TableCell>
                            <TableCell align='center' style={{ width: 160 }}>
                                {row.location.city}
                            </TableCell>
                            <TableCell align='right' style={{ width: 160 }}>
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
            </Table>
            {/* Bottoni pagine */}
            <Container>
                <Grid container columnSpacing={1.4}>
                    <Grid item xs={4} sm={4}>
                        {page !== 1 ?
                            <Button
                                type="submit"
                                fullWidth
                                variant='outlined'
                                sx={{ mt: 3, mb: 2 }}
                                onClick={() => { handlePreviousPage() }}>Previous Page</Button> : <></>}
                    </Grid>

                    <Grid item xs={4} sm={4}>
                        {lastPage != null && !lastPage ?
                            <Button
                                type="submit"
                                fullWidth
                                variant='outlined'
                                sx={{ mt: 3, mb: 2 }}
                                onClick={() => { handleNextPage() }}>Next Page</Button> : <></>}
                    </Grid>

                    <Grid item xs={4} sm={4}>
                        {page !== 1 ?
                            <Button
                                type="submit"
                                fullWidth
                                variant='outlined'
                                sx={{ mt: 3, mb: 2 }}
                                onClick={() => { handleFirstPage() }}>First Page</Button> : <></>}
                    </Grid>
                </Grid>
            </Container>



        </TableContainer>

    );
}