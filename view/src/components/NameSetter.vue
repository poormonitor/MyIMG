<script setup>
import { defineProps, defineEmits } from "vue";
import { ElMessage, ElMessageBox } from "element-plus";
import { Edit } from "@element-plus/icons-vue";
import axios from "../axios";

import "element-plus/es/components/message-box/style/css";

const props = defineProps(["pid", "origin"]);
const emits = defineEmits(["finish"]);

const open = () => {
    ElMessageBox.prompt("Please input the new name", "Edit", {
        confirmButtonText: "OK",
        cancelButtonText: "Cancel",
        inputValue: props.origin,
    })
        .then(({ value }) => {
            axios
                .post("/name", {
                    pid: props.pid,
                    name: value,
                })
                .then((response) => {
                    if (response.data.result == "success") {
                        ElMessage({
                            type: "success",
                            message: `The name of the image is set to: ${value}.`,
                        });
                        emits("finish", props.pid, value);
                    }
                });
        })
        .catch(() => {
            ElMessage({
                type: "info",
                message: "Input canceled",
            });
        });
};
</script>

<template>
    <el-icon @click="open">
        <Edit class="text-sky-600 hover:text-sky-800" />
    </el-icon>
</template>
