import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000";
const userID = localStorage.getItem("userID");
const role = localStorage.getItem("role");
const authorizationObject = {
    "_id": userID,
    "role": role
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


