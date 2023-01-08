import { createRouter, createWebHashHistory } from "vue-router";
import { ElMessage } from "element-plus";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/",
            name: "upload",
            component: () => import("../views/Upload.vue"),
            meta: {
                title: "Upload Picture",
                requiresAuth: true,
                requireAdmin: false,
            },
        },
        {
            path: "/my",
            name: "my",
            component: () => import("../views/My.vue"),
            meta: {
                title: "Manage My Image",
                requiresAuth: true,
                requireAdmin: false,
            },
        },
        {
            path: "/login",
            name: "login",
            component: () => import("../views/Login.vue"),
            meta: {
                title: "Login",
                requiresAuth: false,
                requireAdmin: false,
            },
        },
        {
            path: "/register",
            name: "register",
            component: () => import("../views/Register.vue"),
            meta: {
                title: "Register",
                requiresAuth: false,
                requireAdmin: false,
            },
        },
        {
            path: "/admin",
            name: "admin",
            component: () => import("../views/Admin.vue"),
            redirect: { name: "config" },
            meta: {
                title: "Admin",
                requiresAuth: true,
                requireAdmin: true,
            },
            children: [
                {
                    name: "config",
                    path: "config",
                    component: () => import("../views/Config.vue"),
                },
            ],
        },
    ],
});

router.beforeEach((to, from) => {
    if (to.meta.title) {
        document.title = to.meta.title + " - MyIMG";
    }

    let token = sessionStorage.getItem("access_token_myimg");
    let local_token = localStorage.getItem("access_token_myimg");
    let admin = JSON.parse(sessionStorage.getItem("admin_myimg"));

    if (!token && local_token) {
        sessionStorage.setItem("access_token_myimg", local_token);
    }

    if (to.meta.requiresAuth && !token) {
        return {
            name: "login",
        };
    }

    if (to.meta.requireAdmin && !admin) {
        ElMessage.error("You are not admin.");
        return {
            name: "upload",
        };
    }
});

export default router;
