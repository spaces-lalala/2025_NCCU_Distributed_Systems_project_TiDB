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
  min-height: 70vh;
  padding: var(--spacing-lg);
  background-color: var(--background-color);
}

.confirmation-card {
  max-width: 600px;
  width: 100%;
  padding: var(--spacing-xxl);
  text-align: center;
  background-color: var(--bg-color);
  border-radius: var(--border-radius-large);
  box-shadow: var(--shadow-base);
  border: 1px solid var(--border-lighter);
}

.icon-container {
  margin-bottom: var(--spacing-lg);
}

h1 {
  font-size: var(--font-size-xxxl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.thank-you-message {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xl);
  line-height: 1.6;
}

.order-details {
  background-color: var(--background-light);
  border-radius: var(--border-radius-base);
  padding: var(--spacing-lg);
  margin: var(--spacing-lg) 0;
  border: 1px solid var(--border-light);
}

.order-details p {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  margin: var(--spacing-sm) 0;
  line-height: 1.6;
}

.order-details strong {
  color: var(--text-primary);
  font-weight: var(--font-weight-semibold);
}

.order-details-error {
  background-color: var(--danger-light);
  border: 1px solid var(--danger-color);
  border-radius: var(--border-radius-base);
  padding: var(--spacing-lg);
  margin: var(--spacing-lg) 0;
}

.order-details-error p {
  color: var(--danger-color);
  font-weight: var(--font-weight-semibold);
  margin: 0;
}

.actions {
  margin-top: var(--spacing-xl);
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
  flex-wrap: wrap;
}

.actions .el-button {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);
  border-radius: var(--border-radius-base);
  transition: var(--transition-base);
}

.actions .el-button:hover {
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .order-confirmation-page {
    padding: var(--spacing-md);
  }
  
  .confirmation-card {
    padding: var(--spacing-xl);
  }
  
  h1 {
    font-size: var(--font-size-xxl);
  }
  
  .thank-you-message {
    font-size: var(--font-size-base);
  }
  
  .actions {
    flex-direction: column;
    align-items: center;
  }
  
  .actions .el-button {
    width: 100%;
    max-width: 300px;
  }
}

@media (max-width: 576px) {
  .confirmation-card {
    padding: var(--spacing-lg);
  }
  
  h1 {
    font-size: var(--font-size-xl);
  }
  
  .order-details,
  .order-details-error {
    padding: var(--spacing-md);
  }
}
</style>