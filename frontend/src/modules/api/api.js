import axios from "axios";

const instance = axios.create({
    baseURL: "http://localhost:5000",
});

instance.interceptors.request.use(
    async (config) => {
        //do stuff
        return config;
    },
    (err) => {
        return Promise.reject(err);
    }
);

export default instance;


