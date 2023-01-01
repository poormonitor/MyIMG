<script setup>
import { reactive, ref } from "vue";
import axios from "../axios";
import { useRouter } from "vue-router";
import sha256 from "crypto-js/sha256";

const router = useRouter();
const rememberMe = ref(false);
const loginForm = reactive({
    email: "",
    password: "",
});
const loadingLogin = ref(false);

const rules = {
    email: [
        {
            validator: (rule, value, callback) => {
                if (
                    /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.text(value)
                ) {
                    callback();
                } else {
                    callback(new Error("Check the email if it is correct."));
                }
            },
            trigger: "blur",
        },
    ],
};

const submitForm = () => {
    loadingLogin.value = true;
    axios
        .post("/login", {
            email: loginForm.email,
            password: sha256(loginForm.password).toString(),
            expires: rememberMe.value ? 2592000 : 3600,
        })
        .catch(() => {
            setTimeout(() => {
                loadingLogin.value = false;
            }, 300);
        })
        .then((response) => {
            sessionStorage.setItem(
                "access_token_myimg",
                response.data.access_token
            );
            sessionStorage.setItem("admin_myimg", response.data.admin);
            sessionStorage.setItem("email_myimg", loginForm.email);
            if (rememberMe.value) {
                localStorage.setItem(
                    "access_token_myimg",
                    response.data.access_token
                );
            }
            setTimeout(() => {
                loadingLogin.value = false;
                router.push({ name: "upload" });
            }, 300);
        });
};
</script>

<template>
    <div
        class="mx-auto w-4/5 md:w-2/3 lg:w-1/2 mt-20 py-12 lg:py-16 border-2 rounded-3xl"
    >
        <p class="text-center font-bold text-3xl mb-10">Login</p>
        <el-form
            :model="loginForm"
            :rules="rules"
            label-position="left"
            label-width="33%"
            size="large"
            class="mx-10 md:mx-24 lg:mx-36"
        >
            <el-form-item label="Email">
                <el-input
                    placeholder="Email"
                    autocomplete="email"
                    v-model="loginForm.email"
                />
            </el-form-item>
            <el-form-item label="Password" class="mb-0">
                <el-input
                    type="password"
                    placeholder="Password"
                    autocomplete="current-password"
                    v-model="loginForm.password"
                />
            </el-form-item>
            <div class="relative left-1/3 w-2/3 my-2">
                <el-checkbox
                    v-model="rememberMe"
                    label="Remember Me"
                    size="large"
                />
            </div>
            <p class="text-sm text-center">
                No account?
                <router-link
                    class="text-blue-600 pl-3"
                    :to="{ name: 'register' }"
                    >Register</router-link
                >
            </p>
            <div class="flex justify-center pt-2 lg:pt-4">
                <el-button
                    class="lg:w-2/3 w-full"
                    type="primary"
                    @click="submitForm"
                    :loading="loadingLogin"
                    >Login</el-button
                >
            </div>
        </el-form>
    </div>
</template>
