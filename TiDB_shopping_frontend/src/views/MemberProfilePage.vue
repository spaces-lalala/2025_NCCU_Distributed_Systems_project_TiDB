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
            <el-table-column prop="order_number" label="訂單編號" width="180" sortable />
            <el-table-column prop="order_date" label="訂單日期" width="180" sortable>
              <template #default="{ row }">
                {{ new Date(row.order_date).toLocaleDateString() }}
              </template>
            </el-table-column>
            <el-table-column label="訂單狀態" width="120" align="center">
              <template #default="{ row }">
                <el-tag :type="getStatusTagType(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="total_amount" label="總金額" align="right">
              <template #default="{ row }">
                NT$ {{ row.total_amount ? row.total_amount.toFixed(2) : '0.00' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120" align="center">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="() => router.push({ name: 'OrderConfirmation', params: { orderId: row.id } })">
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
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
}

.profile-card {
  border: none; 
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header h2 {
  margin: 0; 
  color: #303133;
}

.profile-content {
  padding: 10px 0; 
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

.loading-orders, .orders-error {
  padding: 20px;
  text-align: center;
  color: #909399;
  /* background-color: #f7f7f7; */ /* Optional: can remove if skeleton provides enough visual cue */
  border-radius: 4px;
  margin-top: 10px;
}

.order-history-list {
  margin-top: 15px;
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