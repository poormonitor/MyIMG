<script setup>
import { ref, onMounted } from "vue"
import axios from "../axios"
import { copyToClipboard } from "../func";
import { CircleCloseFilled } from "@element-plus/icons-vue";

const myImages = ref([])

onMounted(() => {
    axios.get("/my")
        .then((response) => {
            if (response.data.list) {
                myImages.value = response.data.list
            }
        })
})

const deleteImage = (pid) => {
    axios.post("/delete", {
        pid: pid
    }).then((response) => {
        if (response.data.result == "success") {
            myImages.value = myImages.value.filter(item => item.pid != pid)
        }
    })
}
</script>

<template>
    <p class="ml-8 lg:ml-16 mt-8 lg:mt-12 font-bold text-3xl md:text-4xl">My images</p>
    <p class="text-center text-zinc-400 text-xl md:text-3xl mt-12" v-if="!myImages.length">No images found.</p>
    <div class="grid grid-cols-1 md:grid-cols-2 2xl:grid-cols-3 gap-2 mx-6 md:mx-12 lg:mx-16 mt-6 md:mt-8 lg:mt-10" v-else>
        <div v-for="item in myImages"
            class="pic-card relative flex pl-6 py-1 border hover:bg-slate-100 transition rounded-2xl cursor-pointer"
            :key="item.pid">
            <el-image fit="contain" :src="item.url" class="flex-none self-center h-24 mr-2" lazy />
            <el-popover placement="top-start" title="Copied!" :width="200" trigger="click"
                content="The URL has been copied to the clipboard." :auto-close="1000">
                <template #reference>
                    <div class="flex-1 m-0.5 md:m-2 p-3 break-all" @click="copyToClipboard(item.url)">
                        <p class="text-xs text-indigo-900">{{ item.pid }}</p>
                        <p class="text-xs font-bold text-blue-800">{{ item.indate }}</p>
                        <p class="text-sm mt-2 font-semibold">{{ item.url }}</p>
                    </div>
                </template>
            </el-popover>
            <div class="absolute right-3 top-3 delete-button transition-all">
                <el-popconfirm title="Are you sure to delete this?" @confirm="deleteImage(item.pid)">
                    <template #reference>
                        <el-icon>
                            <CircleCloseFilled class="text-red-500 hover:text-red-700" />
                        </el-icon>
                    </template>
                </el-popconfirm>
            </div>
        </div>
    </div>
</template>

<style scoped>
.pic-card {
    --myimg-card-display: none;
}

.pic-card:hover {
    --myimg-card-display: inline !important;
}

.delete-button {
    display: var(--myimg-card-display);
}
</style>