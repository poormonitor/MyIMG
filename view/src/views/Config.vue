<script setup>
import axios from "../axios";
import { ref, onMounted } from "vue";
import { ElMessage } from "element-plus";

const configData = ref({});
onMounted(() => {
    axios.get("/admin/config").then((response) => {
        if (response.data.config) {
            configData.value = response.data.config;
        }
    });
});

const setConfig = () => {
    axios.post("/admin/setconfig", configData.value).then((response) => {
        if (response.data.result == "success") {
            ElMessage.success("Config has been successfully set.");
        }
    });
};
</script>

<template>
    <p class="mx-10 lg:mx-20 mt-10 text-2xl">Config Management</p>
    <div class="flex justify-center m-8">
        <div class="flex flex-col">
            <el-form label-width="120px">
                <el-form-item
                    :label="item"
                    v-for="item in Object.keys(configData)"
                >
                    <el-input
                        class="w-48 md:w-72 lg:w-96"
                        v-model="configData[item]"
                    ></el-input>
                </el-form-item>
            </el-form>
            <el-button class="w-48 lg:w-64 self-center" type="primary" @click="setConfig"
                >Set</el-button
            >
        </div>
    </div>
</template>
