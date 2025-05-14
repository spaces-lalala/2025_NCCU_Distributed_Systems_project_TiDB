<template>
  <div class="login-page">
    <h2>使用者登入</h2>
    <!-- Login form will go here -->
    <p>登入表單待開發...</p>
    <router-link to="/register">還沒有帳號？前往註冊</router-link>
  </div>
</template>

<script setup lang="ts">
// Logic for login page will go here
import { onMounted } from 'vue';

onMounted(() => {
  console.log('LoginPage mounted');
});
</script>

<style scoped>
.login-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}
</style> 