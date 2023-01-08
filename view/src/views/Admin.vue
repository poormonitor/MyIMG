<script setup>
import { Setting } from "@element-plus/icons-vue";
import { inject } from "vue";

const collapsed = inject("collapsed");
</script>

<template>
    <div class="flex">
        <el-menu
            :router="true"
            :collapse="collapsed"
            default-active="/admin/config"
        >
            <el-menu-item index="/admin/config">
                <el-icon><setting /></el-icon>
                <span>Config Management</span>
            </el-menu-item>
        </el-menu>
        <div class="flex-grow overflow-y-auto admin-container">
            <router-view></router-view>
        </div>
    </div>
</template>

<style>
.admin-container {
    height: calc(100vh - 4rem);
}
</style>
