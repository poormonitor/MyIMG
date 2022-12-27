<script setup>
import { reactive, ref } from "vue"
import axios from "../axios"
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import sha256 from "crypto-js/sha256"

const router = useRouter()
const registerForm = reactive({
    email: "",
    password: "",
    repeat_password: ""
})
const loadingRegister = ref(false)
const form = ref(null)

const rules = reactive({
    email: [{
        validator: (rule, value, callback) => {
            if (/^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/.test(value)) {
                callback()
            } else {
                callback(new Error('Check the email if it is correct.'))
            }
        },
        trigger: "blur"
    }],
    password: [{
        validator: (rule, value, callback) => {
            if (/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/.test(value)) {
                callback()
            } else {
                callback(new Error('Password should include both alphabets and digits, and be longer than 8 characters.'))
            }
        },
        trigger: "blur"
    }],
    repeat_password: [{
        validator: (rule, value, callback) => {
            if (value == registerForm.password) {
                callback()
            } else {
                callback(new Error('Password repeated is not the same as the above.'))
            }
        },
        trigger: "blur"
    }],
})

const submitForm = () => {
    form.value.validate((result) => {
        if (result) {
            loadingRegister.value = true
            axios.post("/register", {
                email: registerForm.email,
                password: sha256(registerForm.password).toString()
            })
                .then((response) => {
                    ElMessage.success("Registered.")
                    setTimeout(() => {
                        loadingRegister.value = false
                        router.push({ name: "login" })
                    }, 1000);
                })
                .catch(() => {
                    setTimeout(() => {
                        loadingRegister.value = false
                    }, 300);
                })
        }
    })
}
</script>

<template>
    <div class="mx-auto w-4/5 md:w-2/3 lg:w-1/2 mt-20 py-12 lg:py-16 border-2 rounded-3xl">
        <p class="text-center font-bold text-3xl mb-10"> Register </p>
        <el-form ref="form" :model="registerForm" :rules="rules" label-position="left" label-width="33%" size="large"
            class="mx-10 md:mx-24 lg:mx-36" :inline-message="true">
            <el-form-item label="Email" prop="email">
                <el-input placeholder="Email" autocomplete="email" v-model="registerForm.email" />
            </el-form-item>
            <el-form-item label="Password" prop="password">
                <el-input type="password" placeholder="Password" autocomplete="new-password"
                    v-model="registerForm.password" />
            </el-form-item>
            <el-form-item label="Repeat Password" prop="repeat_password">
                <el-input type="password" placeholder="Repeat Password" autocomplete="new-password"
                    v-model="registerForm.repeat_password" />
            </el-form-item>
            <p class="text-sm text-center pt-3">
                Already have an account?
                <router-link class="text-blue-600 pl-3" :to="{ name: 'login' }">Login</router-link>
            </p>
            <div class="flex justify-center pt-4 lg:pt-6">
                <el-button class="lg:w-2/3 w-full" type="primary" @click="submitForm"
                    :loading="loadingRegister">Register</el-button>
            </div>
        </el-form>
    </div>
</template>