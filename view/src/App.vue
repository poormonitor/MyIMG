<script setup>
import Header from "./components/Header.vue"
import { useRoute } from "vue-router";
import { computed } from "vue"

const route = useRoute()
const currentRoute = computed(() => route.name)
</script>

<template>
  <Header :key="currentRoute" />
  <router-view />
</template>
