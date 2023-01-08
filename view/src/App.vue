<script setup>
import Header from "./components/Header.vue";
import { useRoute } from "vue-router";
import { computed, ref, watch, provide } from "vue";

const route = useRoute();
const currentRoute = computed(() => route.name);

const darkMode = ref(false);
const collapsed = ref(window.innerWidth <= 768);
provide("collapsed", collapsed);

window.onresize = () => {
    collapsed.value = window.innerWidth <= 768;
};

if (
    window.matchMedia &&
    window.matchMedia("(prefers-color-scheme: dark)").matches
) {
    darkMode.value = true;
}

watch(darkMode, (val) => {
    if (val) document.body.classList.add("dark");
    else document.body.classList.remove("dark");
});
</script>

<template>
    <Header :key="currentRoute" />
    <router-view />
</template>

<style>
html,
body,
#app {
    height: 100%;
}
</style>
