<script setup>
import { ref, onMounted } from "vue";
import axios from "../axios";
import NameSetter from "../components/NameSetter.vue";
import { copyToClipboard } from "../func";
import { CircleCloseFilled, Search } from "@element-plus/icons-vue";

const myImages = ref([]);
const showImages = ref([]);
const copyOptions = ["URL", "Markdown", "HTML", "UBB"];
const copyProp = ref(0);
const searchInput = ref();

onMounted(() => {
    axios.get("/my").then((response) => {
        if (response.data.list) {
            myImages.value = response.data.list;
            showImages.value = myImages.value;
        }
    });
});

const deleteImage = (pid) => {
    axios
        .post("/delete", {
            pid: pid,
        })
        .then((response) => {
            if (response.data.result == "success") {
                myImages.value = myImages.value.filter(
                    (item) => item.pid != pid
                );
                showImages.value = myImages.value;
                ElMessage({
                    type: "success",
                    message: `The image has been deleted.`,
                });
            }
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

const SearchPic = () => {
    showImages.value = myImages.value.filter((item) =>
        item.name.includes(searchInput.value)
    );
};

const highLightName = (name) => {
    if (searchInput.value && name.includes(searchInput.value)) {
        name = name.replace(
            searchInput.value,
            `<font class="text-orange-700 font-semibold">${searchInput.value}</font>`
        );
    }
    return name;
};

const setNewName = (pid, name) => {
    myImages.value.find((item) => item.pid == pid).name = name;
    showImages.value = myImages.value;
};
</script>

<template>
    <div class="mx-8 lg:mx-16 mt-8 lg:mt-12">
        <div class="flex items-center">
            <span class="font-bold text-3xl md:text-4xl">My Images</span>
        </div>
    </div>
    <div class="flex justify-center mt-3">
        <el-input
            v-model="searchInput"
            size="large"
            class="w-64 lg:w-96"
            placeholder="Search"
            :prefix-icon="Search"
            @change="SearchPic"
        />
    </div>
    <div class="flex flex-col md:flex-row gap-y-2 mt-4 items-center justify-center">
        <span class="text-sm text-sky-600 mr-2">Mode of Copy</span>
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
    <p
        class="text-center text-zinc-400 text-xl md:text-3xl mt-12"
        v-if="!showImages.length"
    >
        No images found.
    </p>
    <div
        class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4 gap-x-8 gap-y-4 mx-6 md:mx-12 lg:mx-16 py-6 md:py-8 lg:py-10"
        v-else
    >
        <div
            v-for="item in showImages"
            class="pic-card relative flex pl-6 py-1 border hover:bg-slate-100 hover:shadow-sm transition rounded-2xl cursor-pointer"
            :key="item.pid"
        >
            <el-image
                fit="contain"
                :src="item.url"
                class="flex-none self-center h-24 w-16 mr-2"
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
                        class="flex-1 m-0.5 md:m-2 p-3 break-all"
                        @click="copyToClipboard(getURL(item.url, item.pid))"
                    >
                        <p class="text-xs text-sky-800">{{ item.pid }}</p>
                        <p class="text-xs font-bold text-sky-800">
                            {{ item.indate }}
                        </p>
                        <p
                            class="text-lg mt-1 font-bold"
                            v-html="highLightName(item.name)"
                        ></p>
                        <p
                            class="text-xs font-semibold underline decoration-indigo-500/30"
                        >
                            {{ item.url }}
                        </p>
                    </div>
                </template>
            </el-popover>
            <div class="absolute right-3 top-3 delete-button transition-all">
                <el-popconfirm
                    width="240"
                    title="Are you sure to delete this?"
                    @confirm="deleteImage(item.pid)"
                >
                    <template #reference>
                        <el-icon>
                            <CircleCloseFilled
                                class="text-red-500 hover:text-red-700"
                            />
                        </el-icon>
                    </template>
                </el-popconfirm>
                <NameSetter
                    class="ml-1"
                    :pid="item.pid"
                    :origin="item.name"
                    @finish="setNewName"
                />
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
