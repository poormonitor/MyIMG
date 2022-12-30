<script setup>
import { UploadFilled } from "@element-plus/icons-vue";
import { ElNotification } from "element-plus";
import axios from "../axios";
import { ref, reactive } from "vue";
import { copyToClipboard } from "../func";

const uploadURL = ref("");
const uploadData = reactive({});
const copyOptions = ["URL", "Markdown", "HTML", "UBB"];
const copyProp = ref(0);
const setURL = (raw) => {
    return new Promise((resolve, reject) => {
        let name = raw.name.split(".");
        axios
            .post("/upload_url", {
                name: name.shift(),
                ext: name[0],
            })
            .then((response) => {
                if (response.data.url) {
                    uploadURL.value = response.data.put;
                    uploadData.key = response.data.key;
                    raw.pid = response.data.pid;
                    raw.url = response.data.url;
                    resolve();
                } else {
                    reject("URL request failed.");
                }
            });
    });
};
const sendReceipt = (_, uploadFile) => {
    axios.post("/receipt", {
        pid: uploadFile.raw.pid,
    });
    copyToClipboard(getURL(uploadFile.raw.url, uploadFile.name));
    ElNotification({
        title: "Success",
        message: `The URL of ${uploadFile.name} has been copied!`,
        type: "success",
    });
};

const getURL = (url, name) => {
    switch (copyProp.value) {
        case 0:
            return url;
        case 1:
            return `![${name}](${url})`;
        case 2:
            return `<img src="${url}" />`;
        case 3:
            return `[IMG]${url}[/IMG]`;
    }
};
</script>

<template>
    <div class="mx-auto w-2/3 md:w-1/2 lg:w-1/3">
        <p class="font-bold text-2xl mt-[8vh] mb-6">Upload Images</p>
        <el-upload
            drag
            multiple
            class="mt-4"
            :before-upload="setURL"
            :on-success="sendReceipt"
            :action="uploadURL"
            list-type="picture"
            :data="uploadData"
            accept="image/*"
        >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
                Drop file here or <em>click to upload</em>
            </div>
            <template #tip>
                <div class="el-upload__tip pt-2">
                    Allowed extensions: xbm, tif, pjp, svgz, jpg, jpeg, ico,
                    tiff, gif, svg, jfif, webp, png, bmp, pjpeg, avif.
                </div>
                <div class="flex mt-4 items-center justify-center">
                    <span class="text-xs text-sky-600 mr-2">Mode of Copy</span>
                    <el-radio-group v-model="copyProp" size="small">
                        <el-radio-button
                            v-for="i in copyOptions.length"
                            :key="i - 1"
                            :label="i - 1"
                        >
                            {{ copyOptions[i - 1] }}
                        </el-radio-button>
                    </el-radio-group>
                </div>
            </template>
            <template #file="{ file }">
                <img :src="file.url" class="h-24 m-2" />
                <el-popover
                    placement="top-start"
                    title="Copied!"
                    :width="200"
                    trigger="click"
                    content="The URL has been copied to the clipboard."
                    :hide-after="50"
                >
                    <template #reference>
                        <div
                            class="m-1 p-3 w-0 flex-1 hover:bg-slate-200 transition rounded-2xl cursor-pointer"
                            @click="
                                copyToClipboard(getURL(file.raw.url, file.name))
                            "
                        >
                            <p class="text-xs truncate text-zinc-700">
                                {{ file.raw.pid }}
                            </p>
                            <p
                                class="text-xs truncate font-bold text-indigo-700"
                            >
                                {{ file.name }}
                            </p>
                            <p class="h-10 mt-1 break-all overflow-y-hidden">
                                {{ file.raw.url }}
                            </p>
                        </div>
                    </template>
                </el-popover>
            </template>
        </el-upload>
    </div>
</template>
