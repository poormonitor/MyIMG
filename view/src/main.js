import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

import "./assets/index.css";
import "tailwindcss/src/css/preflight.css";
import "element-plus/es/components/message/style/css";
import "element-plus/es/components/notification/style/css";

const app = createApp(App);

app.use(router);

app.mount("#app");
