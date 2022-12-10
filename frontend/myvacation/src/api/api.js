import axios from "axios";
import useAuth from "../hooks/useAuth";

const BASE_URL = "http://127.0.0.1:5000";
const {userID , role}  = useAuth();
const authorizationObject = {
    "userID" : userID,
    "role" : role
};
const instance = axios.create({
    baseURL: BASE_URL,
    headers: {
        "Access-Control-Allow-Origin" :"*",
        "crossDomain" : true,
        "Authorization" : JSON.stringify(authorizationObject)
    }

});

/*
export const axiosPrivate = axios.create({
    baseURL: BASE_URL,
    headers: { 'Content-Type': 'application/json' },
    withCredentials: true
});
*/

export default instance;


