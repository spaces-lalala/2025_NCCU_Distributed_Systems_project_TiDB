<script setup lang="ts">
import AppNavbar from './components/layout/AppNavbar.vue';
import AppFooter from './components/layout/AppFooter.vue';
</script>

<template>
  <el-container direction="vertical" class="app-layout">
    <AppNavbar />
    <el-main class="app-main-content">
      <div class="page-container">
        <router-view />
      </div>
    </el-main>
    <AppFooter />
  </el-container>
</template>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: var(--bg-page);
}

.app-main-content {
  flex-grow: 1;
  padding: var(--spacing-lg) 0;
  background-color: var(--bg-page);
}

.page-container {
  max-width: var(--container-xl);
  margin: 0 auto;
  padding: 0 var(--spacing-lg);
}
</style>
