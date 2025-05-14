<template>
  <div>
    <h1>商品詳情頁</h1>
    <p>商品 ID: {{ $route.params.id }}</p>
    <!-- Product detail content will go here -->
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from 'vue-router';
// import { ref, onMounted, computed } from 'vue';

const route = useRoute();
// const productId = computed(() => route.params.id);

// onMounted(() => {
//   console.log(`ProductDetailPage mounted for product ID: ${productId.value}`);
// });
</script>

<style scoped>
h1 {
  text-align: center;
  margin-top: 20px;
}
</style> 