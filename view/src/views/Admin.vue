<script setup>
import { Setting } from '@element-plus/icons-vue';
</script>

<template>
    <div class="flex">
        <el-menu :router="true" default-active="/admin/config">
            <el-menu-item index="/admin/config">
                <el-icon><setting /></el-icon>
                <span>Config Management</span>
            </el-menu-item>
        </el-menu>
        <div class="flex-grow">
            <router-view></router-view>
        </div>
    </div>
</template>
