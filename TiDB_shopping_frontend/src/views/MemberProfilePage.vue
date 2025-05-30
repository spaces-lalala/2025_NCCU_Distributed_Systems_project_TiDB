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

        <el-divider content-position="left"><h3>歷史訂單</h3></el-divider>
        <div v-if="isLoadingOrders" class="loading-orders">
          <el-skeleton :rows="5" animated />
        </div>
        <div v-else-if="fetchOrdersError" class="orders-error">
          <el-alert :title="fetchOrdersError" type="error" show-icon :closable="false"></el-alert>
        </div>        <div v-else-if="orders.length > 0" class="order-history-list">
          <el-table :data="orders" style="width: 100%" stripe border>
            <el-table-column prop="order_number" label="訂單編號" min-width="140" sortable show-overflow-tooltip />
            <el-table-column prop="order_date" label="訂單日期" min-width="120" sortable align="center">
              <template #default="{ row }">
                {{ new Date(row.order_date).toLocaleDateString() }}
              </template>
            </el-table-column>
            <el-table-column label="訂單狀態" min-width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="getStatusTagType(row.status)" size="small">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="total_amount" label="總金額" min-width="120" align="right">
              <template #default="{ row }">
                NT$ {{ row.total_amount ? row.total_amount.toFixed(2) : '0.00' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" min-width="100" align="center" fixed="right">
              <template #default="{ row }">
                <el-button 
                  type="primary" 
                  size="small" 
                  @click="() => router.push({ name: 'OrderConfirmation', params: { orderId: row.id } })"
                  class="view-detail-btn"
                >
                  查看詳情
                </el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else>
            <el-empty description="您目前沒有任何歷史訂單。"></el-empty>
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
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';
import { 
  ElMessage, 
  ElMessageBox, 
  ElCard, 
  ElDescriptions, 
  ElDescriptionsItem, 
  ElButton, 
  ElDivider, 
  ElTable, 
  ElTableColumn, 
  ElTag, 
  ElEmpty, 
  ElAlert, 
  ElSkeleton 
} from 'element-plus';

// Import Order type and orderService functions
import type { Order } from '@/types/order';
import { getOrders } from '@/services/orderService';

const authStore = useAuthStore();
const router = useRouter();
const isLoggingOut = ref(false);

const orders = ref<Order[]>([]);
const isLoadingOrders = ref(false);
const fetchOrdersError = ref<string | null>(null);

const fetchOrders = async () => {
  if (!authStore.isAuthenticated) {
    fetchOrdersError.value = '請先登入以查看歷史訂單。';
    // Clear orders if user is not authenticated to prevent showing stale data
    orders.value = []; 
    return;
  }
  isLoadingOrders.value = true;
  fetchOrdersError.value = null;
  try {
    // No need to manually get token, orderService will handle it
    const fetchedOrders = await getOrders();
    orders.value = fetchedOrders;
  } catch (error: any) {
    console.error('Error fetching orders in component:', error);
    // The error from orderService should already be a user-friendly string
    fetchOrdersError.value = error.message || '載入歷史訂單時發生未知錯誤。';
    orders.value = []; // Clear orders on error
  } finally {
    isLoadingOrders.value = false;
  }
};

const getStatusTagType = (status: Order['status']): ('success' | 'info' | 'warning' | 'danger' | '') => {
  switch (status) {
    case 'PENDING': return 'warning';
    case 'PROCESSING': return ''; 
    case 'SHIPPED': return 'info';
    case 'DELIVERED': return 'success';
    case 'CANCELLED': return 'danger';
    default: return 'info';
  }
};

onMounted(() => {
  fetchOrders();
});

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
    authStore.logout();
    ElMessage.success('您已成功登出！');
    router.push('/login');
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('登出時發生錯誤，請稍後再試。');
      console.error('Logout error:', error);
    }
  } finally {
    isLoggingOut.value = false;
  }
};

</script>

<style scoped>
.member-profile-page {
  max-width: var(--container-md);
  margin: var(--spacing-lg) auto;
  padding: var(--spacing-lg);
  min-height: calc(100vh - var(--navbar-height) - var(--footer-height));
}

.profile-card {
  border: none;
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-sm);
  background: var(--card-bg);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-lighter);
}

.card-header h2 {
  margin: 0;
  color: var(--text-primary);
  font-size: var(--font-size-2xl);
  font-weight: var(--font-weight-bold);
}

.profile-content {
  padding: var(--spacing-lg);
}

.el-descriptions {
  margin-bottom: var(--spacing-xl);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  padding: var(--spacing-md);
}

.actions-section {
  margin-top: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
  text-align: left;
  padding: var(--spacing-md);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  border-left: 4px solid var(--danger-color);
}

.el-divider h3 {
  margin: 0;
  font-size: var(--font-size-xl);
  color: var(--text-primary);
  font-weight: var(--font-weight-semibold);
}

.loading-orders, .orders-error {
  padding: var(--spacing-lg);
  text-align: center;
  color: var(--text-secondary);
  background-color: var(--bg-secondary);
  border-radius: var(--border-radius-md);
  margin-top: var(--spacing-md);
  border: 1px solid var(--border-lighter);
}

.order-history-list {
  margin-top: var(--spacing-md);
  background: var(--card-bg);
  border-radius: var(--border-radius-md);
  overflow: hidden;
  border: 1px solid var(--border-lighter);
}

.not-logged-in {
  text-align: center;
  padding: var(--spacing-2xl) var(--spacing-lg);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-lg);
  margin: var(--spacing-lg) 0;
}

.not-logged-in p {
  margin-bottom: var(--spacing-lg);
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  line-height: var(--line-height-relaxed);
}

/* Enhanced table styling */
.order-history-list :deep(.el-table) {
  background: transparent;
  font-size: var(--font-size-sm);
}

.order-history-list :deep(.el-table th) {
  background: var(--bg-secondary);
  color: var(--text-primary);
  font-weight: var(--font-weight-semibold);
  border-bottom: 2px solid var(--border-light);
  padding: var(--spacing-md) var(--spacing-sm);
}

.order-history-list :deep(.el-table td) {
  border-bottom: 1px solid var(--border-lighter);
  padding: var(--spacing-md) var(--spacing-sm);
  vertical-align: middle;
}

.order-history-list :deep(.el-table .el-table__row:hover) {
  background: var(--bg-hover);
}

.order-history-list :deep(.el-button--small) {
  padding: var(--spacing-xs) var(--spacing-sm);
  font-size: var(--font-size-xs);
  border-radius: var(--border-radius-sm);
  min-width: 70px;
}

.order-history-list :deep(.el-tag--small) {
  padding: 2px 6px;
  font-size: var(--font-size-xs);
  border-radius: var(--border-radius-sm);
}

.view-detail-btn {
  white-space: nowrap;
}

/* Enhanced empty state styling */
.order-history-list :deep(.el-empty) {
  padding: var(--spacing-2xl);
  background: var(--bg-secondary);
  border-radius: var(--border-radius-md);
}

.order-history-list :deep(.el-empty__description) {
  color: var(--text-secondary);
  font-size: var(--font-size-md);
}

/* Responsive design */
@media (max-width: 768px) {
  .member-profile-page {
    margin: var(--spacing-md);
    padding: var(--spacing-md);
  }
  
  .card-header {
    padding: var(--spacing-md);
    flex-direction: column;
    gap: var(--spacing-sm);
    text-align: center;
  }
  
  .card-header h2 {
    font-size: var(--font-size-xl);
  }
  
  .profile-content {
    padding: var(--spacing-md);
  }
  
  .not-logged-in {
    padding: var(--spacing-lg) var(--spacing-md);
  }
  
  .order-history-list {
    overflow-x: auto;
  }
  
  .order-history-list :deep(.el-table) {
    min-width: 600px;
    font-size: var(--font-size-xs);
  }
  
  .order-history-list :deep(.el-table th),
  .order-history-list :deep(.el-table td) {
    padding: var(--spacing-sm) var(--spacing-xs);
  }
  
  .order-history-list :deep(.el-button--small) {
    padding: 4px 8px;
    font-size: 10px;
    min-width: 60px;
  }
}

@media (max-width: 480px) {
  .member-profile-page {
    margin: var(--spacing-sm);
    padding: var(--spacing-sm);
  }
  
  .card-header h2 {
    font-size: var(--font-size-lg);
  }
  
  .order-history-list :deep(.el-table) {
    min-width: 500px;
  }
  
  .order-history-list :deep(.el-table th),
  .order-history-list :deep(.el-table td) {
    padding: var(--spacing-xs);
    font-size: 10px;
  }
  
  .order-history-list :deep(.el-button--small) {
    padding: 2px 6px;
    font-size: 9px;
    min-width: 50px;
  }
  
  .order-history-list :deep(.el-tag--small) {
    padding: 1px 4px;
    font-size: 9px;
  }
}
</style>