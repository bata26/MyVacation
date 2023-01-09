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
import Link from '@mui/material/Link';

export default function ToBeApprovedList({ destinationType }) {
    const [last_id, setLast_id] = React.useState(null);
    const [first_id, setFirst_id] = React.useState(null);
    const [page, setPage] = React.useState(1);
    const [toBeApprovedList, setToBeApprovedList] = React.useState(null);
    const navigate = useNavigate();
    const [lastPage, setLastPage] = React.useState(null);


    React.useEffect(() => {
        api.get("/admin/announcements/" + destinationType + "?index=&direction=")
            .then(function (response) {
                if(response && response.data.length > 0) {
                    setToBeApprovedList(response.data);
                    setLast_id(response.data[response.data.length - 1]._id);
                    setFirst_id(response.data[0]._id);
                }
                if (response.data.length === parseInt(process.env.REACT_APP_ADMIN_PAGE_SIZE))
                    setLastPage(false)
            })
            .catch(function (error) {
                alert("Ops, something went wrong :(" + "\n" + error);
            });
    }, []);

    const handlePreviousPage = () => {
        setPage(page - 1)
        const url = "?index=" + first_id + "&direction=previous";
        api.get("/admin/announcements/" + destinationType + url)
            .then(function (response) {
                setToBeApprovedList(response.data);
                setLastPage(false)
                if (response && response.data.length > 0) {
                    setLast_id(response.data[0]._id);
                    setFirst_id(response.data[response.data.length - 1]._id);
                }
            })
            .catch(function (error) {
                alert("Ops, something went wrong :(" + "\n" + error);
            });
    };

    const handleNextPage = () => {
        const url = "?index=" + last_id + "&direction=next";
        api.get("/admin/announcements/" + destinationType + url)
            .then(function (response) {
                if (response && response.data.length > 0) {
                    setLast_id(response.data[response.data.length - 1]._id);
                    setFirst_id(response.data[0]._id);
                    setToBeApprovedList(response.data);
                    setPage(page + 1);
                }
                else {
                    setLastPage(true)
                }
            })
            .catch(function (error) {
                alert("Ops, something went wrong :(" + "\n" + error);
            });

    };

    const handleFirstPage = () => {
        setPage(1);
        api.get("/admin/announcements/" + destinationType + "?index=")
            .then(function (response) {
                setToBeApprovedList(response.data);
                setLast_id(response.data[response.data.length - 1]._id);
                setFirst_id(0);
                setLastPage(false)
            })
            .catch(function (error) {
                alert("Ops, something went wrong :(" + "\n" + error);
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
                        <TableCell align="right" style={{ fontWeight: 'bold' }}>Price</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {toBeApprovedList && true && toBeApprovedList.map((row) => (
                        <TableRow key={row._id}>
                            <TableCell align='left' component="th" scope="row">
                                <Link style={{ cursor: "pointer" }} onClick={() => { navigate("/toApprove/" + row._id + "?type=" + destinationType) }}>
                                    {row.hostID}
                                </Link>
                            </TableCell>
                            <TableCell align='center' component="th" scope="row">
                                {row.name}
                            </TableCell>
                            <TableCell align='center' style={{ width: 160 }}>
                                {row.location.city}
                            </TableCell>
                            <TableCell align='right' style={{ width: 160 }}>
                                {row.price}
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