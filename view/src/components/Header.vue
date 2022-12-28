<script setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from "vue"
import PasswordSetter from './PasswordSetter.vue';
import { logOut } from '../func';

const router = useRouter()
const currentUser = ref(null)
const passwdSetVisible = ref(false)

onMounted(() => {
    currentUser.value = sessionStorage.getItem("email_myimg")
})

const selectHandler = (key) => {
    switch (key) {
        case "1-1":
            router.push({ name: "my" })
            break
        case "1-2":
            passwdSetVisible.value = true
            break
        case "1-3":
            logOut()
            router.push({ name: "login" })
            break
    }
}
</script>

<template>
    <PasswordSetter v-model="passwdSetVisible" />
    <el-menu class="el-menu-demo" default-active="1" mode="horizontal" :ellipsis="false" @select="selectHandler">
        <div class="menu-logo flex items-center mx-4 lg:mx-8">
            <router-link :to="{ name: 'upload' }"
                class="font-bold text-transparent bg-clip-text bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500">
                MyIMG
            </router-link>
        </div>
        <div class="flex-grow" />
        <el-sub-menu index="1" v-if="currentUser">
            <template #title> {{ currentUser }} </template>
            <el-menu-item index="1-1">My Images</el-menu-item>
            <el-menu-item index="1-2">Change Password</el-menu-item>
            <el-menu-item index="1-3">Log Out</el-menu-item>
        </el-sub-menu>
    </el-menu>
</template>

<style>
.menu-logo {
    height: 58px;
    font-size: 22px;
}
</style>