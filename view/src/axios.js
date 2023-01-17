import { ElMessage } from "element-plus";
import { logOut } from "./func";
import axios from "axios";
import router from "./router/index";

const instance = axios.create({
    baseURL: import.meta.env.VITE_API_URL,
    timeout: 5000,
});

instance.interceptors.request.use(
    (config) => {
        let token = sessionStorage.getItem("access_token_myimg");
        if (token) {
            config.headers.Authorization = "Bearer " + token;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

instance.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (!error.response) {
            ElMessage.error("Network error.");
        } else if (error.response.status == 401) {
            logOut();
            ElMessage.error("Login expires. Please login first.");
            setTimeout(() => {
                router.push({ name: "login" });
                location.reload();
            }, 1000);
        } else if (error.response.status == 422) {
            ElMessage.error("Params error.");
        } else {
            ElMessage.error(error.response.data.detail);
        }
        return Promise.reject(error);
    }
);

export default instance;
