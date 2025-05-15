<template>
  <el-footer class="app-footer">
    <p>&copy; {{ currentYear }} 購物網站. All Rights Reserved.</p>
    <p>
      <a href="/about-us">關於我們</a> | 
      <a href="/contact">聯絡我們</a> | 
      <a href="/privacy-policy">隱私權政策</a>
    </p>
  </el-footer>
</template>

<script lang="ts" setup>
import { computed } from 'vue';

const currentYear = computed(() => new Date().getFullYear());
</script>

<style scoped>
.app-footer {
  background-color: #f0f2f5; /* A light grey background */
  color: #606266; /* Element Plus secondary text color */
  padding: 20px;
  text-align: center;
  border-top: 1px solid #e0e0e0;
  font-size: 0.9em;
}

.app-footer p {
  margin: 5px 0;
}

.app-footer a {
  color: #409EFF; /* Element Plus primary color for links */
  text-decoration: none;
  margin: 0 5px;
}

.app-footer a:hover {
  text-decoration: underline;
}
</style> 