<template>
  <div class="best-sellers-page">
    <h2>熱銷排行榜</h2>
    <p>熱銷商品列表待開發...</p>
  </div>
</template>

<script setup lang="ts">
// Logic for best sellers page will go here
import { onMounted } from 'vue';

onMounted(() => {
  console.log('BestSellersPage mounted');
});
</script>

<style scoped>
.best-sellers-page {
  padding: 20px;
  text-align: center;
}
</style> 