<template>
  <div class="not-found-page">
    <h2>404 - 頁面未找到</h2>
    <p>您所尋找的頁面不存在。</p>
    <router-link to="/">返回首頁</router-link>
  </div>
</template>

<script setup lang="ts">
// Logic for not found page will go here
import { onMounted } from 'vue';

onMounted(() => {
  console.log('NotFoundPage mounted');
});
</script>

<style scoped>
.not-found-page {
  padding: 20px;
  text-align: center;
}
</style> 