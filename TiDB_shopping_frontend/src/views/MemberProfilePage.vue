<template>
  <div class="member-profile-page">
    <el-card class="profile-card" shadow="never">
      <template #header>
        <div class="card-header">
          <h2>會員中心</h2>
        </div>
      </template>

      <div v-if="authStore.isAuthenticated && authStore.user" class="profile-content">
        <el-descriptions title="基本資訊" :column="1" border>
          <el-descriptions-item label="會員名稱">{{ authStore.user.name }}</el-descriptions-item>
          <el-descriptions-item label="Email">{{ authStore.user.email }}</el-descriptions-item>
          <!-- Add more user details here if available and needed -->
        </el-descriptions>

        <div class="actions-section">
          <el-button type="danger" @click="handleLogout" :loading="isLoggingOut">登出帳號</el-button>
        </div>

        <!-- Placeholder for future order history -->
        <el-divider content-position="left"><h3>歷史訂單</h3></el-divider>
        <div class="order-history-placeholder">
          <p>您的歷史訂單將會顯示在這裡。(功能待開發)</p>
        </div>

      </div>
      <div v-else class="not-logged-in">
        <p>您尚未登入，請先登入以查看會員資訊。</p>
        <router-link to="/login">
          <el-button type="primary">前往登入</el-button>
        </router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox, ElCard, ElDescriptions, ElDescriptionsItem, ElButton, ElDivider } from 'element-plus';

const authStore = useAuthStore();
const router = useRouter();
const isLoggingOut = ref(false);

const handleLogout = async () => {
  isLoggingOut.value = true;
  try {
    await ElMessageBox.confirm(
      '您確定要登出嗎？',
      '確認登出',
      {
        confirmButtonText: '確定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    );
    // Perform logout action from auth store
    authStore.logout();
    ElMessage.success('您已成功登出！');
    // Redirect to login page or home page after logout
    router.push('/login');
  } catch (error) {
    // If error is 'cancel', it means user clicked cancel in ElMessageBox
    if (error !== 'cancel') {
      ElMessage.error('登出時發生錯誤，請稍後再試。');
      console.error('Logout error:', error);
    } else {
      ElMessage.info('已取消登出操作。');
    }
  } finally {
    isLoggingOut.value = false;
  }
};

// onMounted(() => {
//   if (!authStore.isAuthenticated) {
//     // This check is mostly redundant if route guards are effective
//     // router.push({ name: 'Login', query: { redirect: route.fullPath } });
//   }
//   console.log('MemberProfilePage mounted, user:', authStore.user);
// });

</script>

<style scoped>
.member-profile-page {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
}

.profile-card {
  border: none; /* Remove default card border if using custom layout */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0; /* Remove default margin from h2 */
  color: #303133;
}

.profile-content {
  padding: 10px 0; /* Add some padding if header is used */
}

.el-descriptions {
  margin-bottom: 30px;
}

.actions-section {
  margin-top: 20px;
  margin-bottom: 30px;
  text-align: left;
}

.el-divider h3 {
  margin: 0;
  font-size: 1.2em;
  color: #606266;
}

.order-history-placeholder {
  padding: 20px;
  text-align: center;
  color: #909399;
  background-color: #f7f7f7;
  border-radius: 4px;
  margin-top: 10px;
}

.not-logged-in {
  text-align: center;
  padding: 40px 20px;
}
.not-logged-in p {
  margin-bottom: 20px;
  font-size: 1.1em;
}
</style> 