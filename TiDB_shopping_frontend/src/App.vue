<script setup lang="ts">
import AppNavbar from './components/layout/AppNavbar.vue';
import AppFooter from './components/layout/AppFooter.vue';
</script>

<template>
  <el-container direction="vertical" class="app-layout">
    <AppNavbar />
    <el-main class="app-main-content">
      <router-view />
    </el-main>
    <AppFooter />
  </el-container>
</template>

<style scoped>
.app-layout {
  min-height: 100vh; /* Ensure layout takes at least full viewport height */
  display: flex;
  flex-direction: column;
}

.app-main-content {
  flex-grow: 1; /* Allow main content to take available space */
  padding: 20px; /* Add some padding around the main content area */
}
</style>

<style>
/* Global styles or resets can go here if not in a separate CSS file like style.css */
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji', 'Segoe UI Symbol',
    'Noto Color Emoji';
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

#app {
  /* Ensure #app itself doesn't interfere with full height layout if it has styles */
}
</style>
