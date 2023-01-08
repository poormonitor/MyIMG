<script setup>
import { useRouter } from "vue-router";
import { ref, onMounted } from "vue";
import { ArrowDown } from "@element-plus/icons-vue";
import PasswordSetter from "./PasswordSetter.vue";
import { logOut } from "../func";

const router = useRouter();
const currentUser = ref(null);
const passwdSetVisible = ref(false);

onMounted(() => {
    currentUser.value = sessionStorage.getItem("email_myimg");
});

const selectHandler = (key) => {
    switch (key) {
        case "1":
            router.push({ name: "my" });
            break;
        case "2":
            passwdSetVisible.value = true;
            break;
        case "3":
            router.push({ name: "config" });
            break;
        case "4":
            logOut();
            router.push({ name: "login" });
            break;
    }
};
</script>

<template>
    <PasswordSetter v-model="passwdSetVisible" />
    <el-menu
        class="el-menu-demo h-16"
        default-active="1"
        mode="horizontal"
        :ellipsis="false"
    >
        <div class="menu-logo flex items-center mx-4 lg:mx-8">
            <router-link
                :to="{ name: 'upload' }"
                class="font-bold text-transparent bg-clip-text bg-gradient-to-tr from-indigo-500 via-purple-500 to-pink-500"
            >
                MyIMG
            </router-link>
        </div>
        <div class="flex-grow" />
        <el-dropdown
            class="self-center"
            @command="selectHandler"
            v-if="currentUser"
        >
            <span
                class="transition hover:text-blue-500 mr-4 flex items-center gap-x-1"
            >
                {{ currentUser }}
                <el-icon><arrow-down /></el-icon>
            </span>
            <template #dropdown>
                <el-dropdown-menu>
                    <el-dropdown-item command="1">My Images</el-dropdown-item>
                    <el-dropdown-item command="2">
                        Change Password
                    </el-dropdown-item>
                    <el-dropdown-item command="3" divided>
                        Admin
                    </el-dropdown-item>
                    <el-dropdown-item command="4" divided
                        >Log Out</el-dropdown-item
                    >
                </el-dropdown-menu>
            </template>
        </el-dropdown>
    </el-menu>
</template>

<style>
.menu-logo {
    height: 58px;
    font-size: 22px;
}
</style>
