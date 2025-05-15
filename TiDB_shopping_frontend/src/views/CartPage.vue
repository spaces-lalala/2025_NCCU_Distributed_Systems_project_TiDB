<template>
  <div class="cart-page">
    <h1>您的購物車</h1>

    <div v-if="cartStore.isEmpty" class="empty-cart-container">
      <el-empty description="您的購物車目前是空的">
        <router-link to="/products">
          <el-button type="primary">前往購物</el-button>
        </router-link>
      </el-empty>
    </div>

    <div v-else class="cart-content">
      <el-table :data="cartStore.getCartItems" style="width: 100%" class="cart-table">
        <el-table-column label="商品圖片" width="120">
          <template #default="{ row }">
            <img :src="row.imageUrl" :alt="row.name" class="cart-item-image" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商品名稱" min-width="180"></el-table-column>
        <el-table-column label="單價" width="120">
          <template #default="{ row }">
            NT$ {{ row.price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="數量" width="180">
          <template #default="{ row }">
            <el-input-number
              :model-value="row.quantity"
              @change="(currentValue) => handleQuantityChange(row.id, currentValue)"
              :min="1"
              :max="row.stock" 
              size="small"
              controls-position="right"
            />
          </template>
        </el-table-column>
        <el-table-column label="小計" width="120">
          <template #default="{ row }">
            NT$ {{ (row.price * row.quantity).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="danger" :icon="Delete" circle plain @click="confirmRemoveItem(row.id)" />
          </template>
        </el-table-column>
      </el-table>

      <div class="cart-summary">
        <div class="summary-actions">
            <el-button type="danger" plain @click="confirmClearCart">清空購物車</el-button>
        </div>
        <div class="summary-totals">
          <p class="total-items">總計 {{ cartStore.totalItemQuantity }} 件商品</p>
          <p class="total-price">總金額: <span class="price-value">NT$ {{ cartStore.totalPrice.toFixed(2) }}</span></p>
          <el-button type="primary" size="large" @click="goToCheckout" class="checkout-button">前往結帳</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useCartStore } from '@/store/cart';
import type { CartItem } from '@/store/cart'; // Import CartItem if needed for type checking in handlers
import { ElMessage, ElMessageBox, ElInputNumber, ElTable, ElTableColumn, ElButton, ElEmpty, ElIcon } from 'element-plus';
import { Delete } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

const cartStore = useCartStore();
const router = useRouter();

const handleQuantityChange = (productId: string, newQuantity: number | undefined) => {
  if (newQuantity === undefined || newQuantity < 1) {
    // If undefined or less than 1, treat as attempt to remove or invalid input, 
    // consider prompting to remove or setting to 1.
    // For now, we rely on el-input-number's min prop for direct input.
    // If the change event fires with undefined, it might mean the field was cleared.
    // We might want to remove the item or set quantity to 1.
    // For simplicity, if newQuantity is undefined, we can re-fetch the current quantity or set to 1
    const item = cartStore.getCartItems.find(i => i.id === productId);
    if (item) cartStore.updateItemQuantity(productId, item.quantity); // revert or set to 1
    return;
  }
  cartStore.updateItemQuantity(productId, newQuantity);
  ElMessage.success('購物車數量已更新');
};

const confirmRemoveItem = (productId: string) => {
  ElMessageBox.confirm(
    '您確定要從購物車中移除此商品嗎？',
    '確認移除',
    {
      confirmButtonText: '確定',
      cancelButtonText: '取消',
      type: 'warning',
    }
  ).then(() => {
    cartStore.removeItem(productId);
    ElMessage.success('商品已從購物車移除');
  }).catch(() => {
    // User cancelled
    ElMessage.info('已取消移除');
  });
};

const confirmClearCart = () => {
  if (cartStore.isEmpty) {
    ElMessage.info('購物車已經是空的了');
    return;
  }
  ElMessageBox.confirm(
    '您確定要清空整個購物車嗎？此操作無法復原。',
    '確認清空購物車',
    {
      confirmButtonText: '確定清空',
      cancelButtonText: '取消',
      type: 'warning',
      draggable: true,
    }
  ).then(() => {
    cartStore.clearCart();
    ElMessage.success('購物車已清空');
  }).catch(() => {
    ElMessage.info('已取消清空操作');
  });
};

const goToCheckout = () => {
  // For now, just a placeholder. Later, this will navigate to the checkout page.
  if (cartStore.isEmpty) {
    ElMessage.warning('您的購物車是空的，請先加入商品再結帳。');
    return;
  }
  ElMessage.info('準備前往結帳頁面... (功能待實現)');
  router.push('/checkout'); // Navigate to checkout page
};

</script>

<style scoped>
.cart-page {
  max-width: 1000px;
  margin: 20px auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.empty-cart-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 300px; /* Ensure it takes some space */
}

.cart-item-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.cart-table {
  margin-bottom: 30px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}

.cart-table .el-table__header-wrapper th {
  background-color: #f5f7fa;
  color: #909399;
  font-weight: bold;
}

.cart-summary {
  display: flex;
  justify-content: space-between;
  align-items: flex-start; /* Align items to the top */
  padding: 20px;
  background-color: #fff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.summary-actions {
  /* Takes available space, pushing totals to the right */
}

.summary-totals {
  text-align: right;
}

.total-items {
  font-size: 1em;
  color: #606266;
  margin-bottom: 8px;
}

.total-price {
  font-size: 1.2em;
  color: #303133;
  margin-bottom: 20px;
  font-weight: bold;
}

.total-price .price-value {
  color: #f56c6c; /* Highlight price */
  font-size: 1.3em;
}

.checkout-button {
  width: 100%;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .cart-summary {
    flex-direction: column-reverse; /* Stack totals above actions on small screens */
    align-items: stretch;
  }
  .summary-actions {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
  .summary-totals {
    text-align: center;
  }
  .checkout-button {
    margin-top: 10px;
  }
}
</style> 