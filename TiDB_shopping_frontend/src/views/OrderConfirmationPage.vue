<template>
  <div class="order-confirmation-page">
    <el-card shadow="always" class="confirmation-card">
      <div class="icon-container">
        <el-icon :size="60" color="#67C23A"><CircleCheckFilled /></el-icon>
      </div>
      <h1>訂單提交成功！</h1>
      <p class="thank-you-message">感謝您的購買，我們已收到您的訂單。</p>
      
      <div v-if="displayOrderNumber" class="order-details">
        <p>您的訂單編號是：<strong>{{ displayOrderNumber }}</strong></p>
        <p>我們會盡快為您處理，您可以隨時在會員中心追蹤訂單狀態。</p>
      </div>

      <div v-else class="order-details-error">
        <p>無法獲取訂單編號，請聯繫客服。</p>
      </div>

      <div class="actions">
        <router-link to="/">
          <el-button type="primary" size="large">返回首頁</el-button>
        </router-link>
        <router-link :to="{ name: 'MemberProfile' }" v-if="authStore.isAuthenticated">
          <el-button type="default" size="large" style="margin-left: 10px;">查看我的訂單</el-button>
        </router-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import { ElCard, ElIcon, ElButton } from 'element-plus';
import { CircleCheckFilled } from '@element-plus/icons-vue';

const route = useRoute();
const authStore = useAuthStore();
const orderId = ref<string | null>(null);
const displayOrderNumber = ref<string | null>(null);

onMounted(() => {
  const paramsOrderId = route.params.orderId;
  const paramsOrderNumber = route.params.orderNumber;

  if (paramsOrderNumber) {
    displayOrderNumber.value = Array.isArray(paramsOrderNumber) ? paramsOrderNumber[0] : paramsOrderNumber;
  } else if (paramsOrderId) {
    displayOrderNumber.value = Array.isArray(paramsOrderId) ? paramsOrderId[0] : paramsOrderId;
  }

  if (paramsOrderId) {
    orderId.value = Array.isArray(paramsOrderId) ? paramsOrderId[0] : paramsOrderId;
  } 
  
  if (!displayOrderNumber.value) {
    console.warn('No orderId or orderNumber found in route params for OrderConfirmationPage');
  }
});
</script>

<style scoped>
.order-confirmation-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh; /* Make it take up a good portion of the viewport */
  padding: 20px;
  background-color: #f4f4f5; /* Light background for the page */
}

.confirmation-card {
  max-width: 600px;
  width: 100%;
  padding: 30px;
  text-align: center;
}

.icon-container {
  margin-bottom: 20px;
}

h1 {
  font-size: 2em;
  color: #303133;
  margin-bottom: 10px;
}

.thank-you-message {
  font-size: 1.1em;
  color: #606266;
  margin-bottom: 25px;
}

.order-details p {
  font-size: 1em;
  color: #909399;
  margin: 8px 0;
}

.order-details strong {
  color: #303133;
}

.order-details-error p {
  color: #F56C6C;
  font-weight: bold;
}

.actions {
  margin-top: 30px;
}

.actions .el-button {
  padding: 12px 25px;
}
</style> 