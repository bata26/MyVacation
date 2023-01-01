import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000";
const userID = localStorage.getItem("userID");
const role = localStorage.getItem("role");
const username = localStorage.getItem("username");
const authorizationObject = {
    "_id": userID,
    "role": role,
    "username" : username
};
const instance = axios.create({
    baseURL: BASE_URL,
    headers: {
        "Access-Control-Allow-Origin" :"*",
        "crossDomain" : true,
        "Authorization" : JSON.stringify(authorizationObject),
        "Content-Type" : "application/json"
    }

});

export default instance;


