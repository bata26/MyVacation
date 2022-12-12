import * as React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Title from './title';
import api from "../../api/api";
import Grid from "@mui/material/Grid";
import {TextField} from "@mui/material";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import TableContainer from "@mui/material/TableContainer";
import Paper from "@mui/material/Paper";
import TableFooter from "@mui/material/TableFooter";
import {useNavigate} from "react-router-dom";
import useAuth from '../../hooks/useAuth';



export default function UsersList() {
    const {auth} = useAuth();
    const [last_id, setLast_id] = React.useState(null);
    const [first_id, setFirst_id] = React.useState(null);
    const [page, setPage] = React.useState(1);
    const navigate = useNavigate();
    const [userList, setUserList] = React.useState(null);
    const [name, setName] = React.useState("");
    const [surname, setSurname] = React.useState("");
    const [id, setId] = React.useState("");
    const [lastPage, setLastPage] = React.useState(null);

    React.useEffect(() => {
        console.log(auth);
        api.get("/users?index=")
            .then(function (response) {
                setUserList(response.data);
                setLast_id(response.data[response.data.length -1]._id);
                setFirst_id(response.data[0]._id);
                console.log(response);
                if(response.data.length === 2)
                    setLastPage(false)
            })
            .catch(function (error) {
                console.log(error);
            });
    }, []);

    const handleSearch = (event) => {
        event.preventDefault();
        setPage(1);
        const data = new FormData(event.currentTarget);
        console.log({
            userId: data.get('userId'),
            name: data.get('name'),
            surname: data.get('surname')
        });
        const name = data.get('name');
        const surname = data.get('surname');
        const id = data.get('userId');

        const url ="?id=" + id + "&name=" + name + "&surname=" + surname + "&index=";

        console.log(url);
        api.get("/users"+url)
            .then(function (response) {
                setUserList(response.data);
                setLast_id(response.data[4]._id);
                setFirst_id(response.data[0]);
                console.log(response.data);
            })
            .catch(function (error) {
                console.log(error);
            });
    };

    const handlePreviousPage = () => {
        setPage(page-1)
        const url ="?id=" + id + "&name=" + name + "&surname=" + surname + "&index=" + first_id + "&direction=previous";
        console.log(url);
        api.get("/users"+url)
            .then(function (response) {
                setUserList(response.data);
                setLastPage(false)
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
        const url ="?id=" + id + "&name=" + name + "&surname=" + surname + "&index=" + last_id + "&direction=next";
        console.log(url);
        api.get("/users"+url)
            .then(function (response) {
                if (response && response.data.length > 0 ) {
                    setLast_id(response.data[response.data.length - 1]._id);
                    setFirst_id(response.data[0]._id);
                    setUserList(response.data);
                    setPage(page+1);
                }
                else{
                    setLastPage(true)
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
        const url ="?id=" + id + "&name=" + name + "&surname=" + surname + "&index=";

        console.log(url);
        api.get("/users"+url)
            .then(function (response) {
                setUserList(response.data);
                setLast_id(response.data[response.data.length - 1]._id);
                setFirst_id(0);
                console.log(response.data);
                setLastPage(false)
            })
            .catch(function (error) {
                console.log(error);
                console.log(first_id)
                console.log(last_id)
            });

    };

    const emptyRows =
        page > 1 ? Math.max(0, 2 - userList ? userList.length : 0) : 0;

    return (

        <TableContainer component={Paper}>
            <Title>Users list</Title>
            <Box component="form" onSubmit={handleSearch} noValidate sx={{ mt: 1 }}>
                <Grid container columnSpacing={1.4}>
                    <Grid item xs={6} sm={2}>
                        <TextField
                            fullWidth
                            id="userId"
                            name="userId"
                            label="Id"
                        />
                    </Grid>
                    <Grid item xs={6} sm={2}>
                        <TextField
                            fullWidth
                            id="name"
                            name="name"
                            label="Name"
                        />
                    </Grid>
                    <Grid item xs={4} sm={2}>
                        <TextField
                            fullWidth
                            id="surname"
                            name="surname"
                            label="Surname"
                        />
                    </Grid>
                </Grid>
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    sx={{ mt: 3, mb: 2 }}
                >
                    Search
                </Button>
            </Box>
            <Table sx={{ minWidth: 500 }} aria-label="custom pagination table">
                <TableHead>
                    <TableRow>
                        <TableCell>Id</TableCell>
                        <TableCell>Name</TableCell>
                        <TableCell>Surname</TableCell>
                        <TableCell>Date Of Birth</TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    { userList && userList.map((row) => (
                        <TableRow key={row._id} onClick={()=>{navigate("/profile/"+row._id)}} selected={true}>
                            <TableCell component="th" scope="row">
                                {row._id}
                            </TableCell>
                            <TableCell component="th" scope="row">
                                {row.name}
                            </TableCell>
                            <TableCell style={{ width: 160 }} align="right">
                                {row.surname}
                            </TableCell>
                            <TableCell style={{ width: 160 }} align="right">
                                {row.dateOfBirth}
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
                            {lastPage!= null ? !lastPage && <Button onClick={() => {handleNextPage()}}>Next</Button> : <></>}
                            {page !== 1 ? <Button onClick={() => {handleFirstPage()}}> First</Button> : <></>}
                        </TableCell>
                    </TableRow>
                </TableFooter>
            </Table>
        </TableContainer>
    );
}