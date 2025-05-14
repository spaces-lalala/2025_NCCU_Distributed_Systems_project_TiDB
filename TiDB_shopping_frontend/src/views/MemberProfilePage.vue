<template>
  <div class="member-profile-page">
    <h2>會員中心</h2>
    <p>會員資訊及歷史訂單待開發...</p>
  </div>
</template>

<script setup lang="ts">
// Logic for member profile page will go here
import { onMounted } from 'vue';

onMounted(() => {
  console.log('MemberProfilePage mounted');
});
</script>

<style scoped>
.member-profile-page {
  padding: 20px;
  text-align: center;
}
</style> 