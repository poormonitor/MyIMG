<script setup>
import { UploadFilled } from "@element-plus/icons-vue";
import { ElMessage } from "element-plus";
import mime from "mime";
import axios from "../axios";
import { ref, reactive, onMounted } from "vue";
import { copyToClipboard } from "../func";

const uploadURL = ref("");
const uploadData = reactive({});
const copyOptions = ["URL", "Markdown", "HTML", "UBB"];
const copyProp = ref(0);
const uploadRef = ref(null);

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
    ElMessage({
        message: "The URL of the image has been copied!",
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

const CopyClipboard = () => {
    if (navigator.clipboard) {
        navigator.clipboard.read().then((clipboardItems) => {
            for (const item of clipboardItems) {
                for (const fileType of item.types) {
                    if (fileType.indexOf("image") !== -1) {
                        item.getType(fileType).then((blob) => {
                            const filename =
                                "image." + mime.getExtension(fileType);
                            const file = new File([blob], filename, {
                                type: fileType,
                            });
                            uploadRef.value.handleStart(file);
                            uploadRef.value.submit();
                            return;
                        });
                    }
                }
            }
        });
    } else {
        ElMessage({
            message:
                "The browser does not support Clipboard API. Use Ctrl + V instead.",
            type: "info",
        });
    }
};

onMounted(() => {
    window.addEventListener("paste", (event) => {
        const items = (event.clipboardData || event.originalEvent.clipboardData)
            .items;

        for (const item of items) {
            if (item.type.indexOf("image") !== -1) {
                const blob = item.getAsFile();
                uploadRef.value.handleStart(blob);
                uploadRef.value.submit();
                event.preventDefault();
                return;
            }
        }
    });
});
</script>

<template>
    <div class="mx-8 md:mx-auto md:w-1/2 xl:w-5/12">
        <p class="font-bold text-2xl mt-[8vh] mb-6">Upload Images</p>
        <el-upload
            drag
            multiple
            class="mt-4 mb-12"
            :before-upload="setURL"
            :on-success="sendReceipt"
            :action="uploadURL"
            list-type="picture"
            :data="uploadData"
            ref="uploadRef"
            accept="image/*"
        >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
                Drop file here or <em>click to upload</em>
            </div>
            <template #tip>
                <div class="flex items-center justify-center pt-2">
                    <el-button @click="CopyClipboard" size="small">
                        Copy Clipboard
                    </el-button>
                </div>
                <div class="el-upload__tip pt-2">
                    Allowed extensions: xbm, tif, pjp, svgz, jpg, jpeg, ico,
                    tiff, gif, svg, jfif, webp, png, bmp, pjpeg, avif.
                </div>
                <div
                    class="flex flex-col md:flex-row gap-y-2 pt-4 pb-4 items-center justify-center"
                >
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
                <el-image
                    fit="contain"
                    :src="file.url"
                    class="flex-none self-center h-24 w-16 mx-1"
                    lazy
                />
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
                            class="m-1 p-4 w-0 flex-1 hover:bg-slate-200 transition rounded-2xl cursor-pointer"
                            @click="
                                copyToClipboard(getURL(file.raw.url, file.name))
                            "
                        >
                            <p class="text-xs truncate text-sky-800">
                                {{ file.raw.pid }}
                            </p>
                            <p
                                class="text-sm truncate mb-1 font-bold text-sky-800"
                            >
                                {{ file.name }}
                            </p>
                            <p
                                class="text-xs font-semibold underline decoration-indigo-500/30"
                            >
                                {{ file.raw.url }}
                            </p>
                        </div>
                    </template>
                </el-popover>
            </template>
        </el-upload>
    </div>
</template>
