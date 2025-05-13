<template>
  <el-footer class="app-footer">
    <p>&copy; {{ currentYear }} TiDB Shopping Demo. All rights reserved.</p>
    <p>
      Powered by Vue.js, Element Plus, and TiDB.
    </p>
  </el-footer>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const currentYear = computed(() => new Date().getFullYear());
</script>

<style scoped>
.app-footer {
  text-align: center;
  padding: 20px;
  border-top: 1px solid #e4e7ed; /* Element Plus divider color */
  color: #909399; /* Element Plus secondary text color */
  font-size: 0.9rem;
  margin-top: auto; /* Push footer to the bottom if content is short */
}

.app-footer p {
  margin: 5px 0;
}
</style> 