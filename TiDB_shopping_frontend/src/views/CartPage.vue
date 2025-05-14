<template>
  <div class="cart-page">
    <h1 class="page-title">我的購物車</h1>

    <el-empty description="您的購物車還是空的，快去選購商品吧！" v-if="cartStore.isEmpty">
      <el-button type="primary" @click="router.push('/products')">去逛逛</el-button>
    </el-empty>

    <div v-else class="cart-content">
      <el-table :data="cartStore.items" style="width: 100%" class="cart-table">
        <el-table-column label="商品圖片" width="120">
          <template #default="{ row }">
            <img :src="row.image_url || defaultProductImage" alt="商品圖片" class="product-thumbnail" @error="onImageError" />
          </template>
        </el-table-column>
        <el-table-column prop="name" label="商品名稱" min-width="200"></el-table-column>
        <el-table-column label="單價" width="120">
          <template #default="{ row }">
            ￥{{ row.price.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="數量" width="180">
          <template #default="{ row }">
            <el-input-number 
              v-model="row.quantity" 
              :min="1" 
              :max="row.stock || 99" /* Assume stock is available on cart item, or a sensible max */
              size="small"
              @change="(currentValue, oldValue) => handleQuantityChange(row.id, currentValue, oldValue)"
            />
          </template>
        </el-table-column>
        <el-table-column label="小計" width="120">
          <template #default="{ row }">
            ￥{{ (row.price * row.quantity).toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button type="danger" :icon="Delete" circle @click="handleRemoveItem(row.id)" />
          </template>
        </el-table-column>
      </el-table>

      <div class="cart-summary">
        <div class="summary-row">
          <span>商品總數:</span>
          <span class="summary-value">{{ cartStore.cartItemCount }} 件</span>
        </div>
        <div class="summary-row total-price-row">
          <span>總金額:</span>
          <span class="summary-value total-price">￥{{ cartStore.cartTotalPrice.toFixed(2) }}</span>
        </div>
        <div class="summary-actions">
          <el-button type="danger" plain @click="confirmClearCart">清空購物車</el-button>
          <el-button type="primary" size="large" @click="goToCheckout" :disabled="cartStore.isEmpty">前往結帳</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import { useCartStore } from '@/store/cart';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Delete } from '@element-plus/icons-vue';
import type { Product } from '@/types/domain'; // For type hint if needed, though store handles it

const router = useRouter();
const cartStore = useCartStore();

const defaultProductImage = 'https://via.placeholder.com/80x80.png?text=Img';

const onImageError = (event: Event) => {
  const imgElement = event.target as HTMLImageElement;
  imgElement.src = defaultProductImage;
};

const handleQuantityChange = (productId: string | number, newQuantity: number, oldQuantity: number | undefined) => {
  // ElInputNumber might emit null or undefined if input is cleared, ensure it's a number
  if (typeof newQuantity === 'number' && newQuantity > 0) {
    cartStore.updateItemQuantity(productId, newQuantity);
  } else if (typeof newQuantity !== 'number' && typeof oldQuantity === 'number') {
    // If newQuantity is not a number (e.g., cleared input), revert to oldQuantity or 1
    // This case needs careful handling based on ElInputNumber behavior with invalid input
    // For simplicity, we might let the store handle invalid quantities (e.g., clamping to 1 or stock)
    // Or, find the item and reset its quantity if it became invalid. Here, we assume the store setter handles it.
    // Let's assume the store clamps it, or we could manually set it to a valid minimum like 1.
    const item = cartStore.items.find(i => i.id === productId);
    if (item) {
        item.quantity = oldQuantity || 1; // Revert or set to 1 if input became invalid
        cartStore.updateItemQuantity(productId, item.quantity);
    }
  }
};

const handleRemoveItem = (productId: string | number) => {
  cartStore.removeItem(productId);
  ElMessage.success('商品已從購物車移除');
};

const confirmClearCart = () => {
  ElMessageBox.confirm(
    '您確定要清空購物車中的所有商品嗎？此操作無法復原。',
    '清空購物車',
    {
      confirmButtonText: '確定清空',
      cancelButtonText: '取消',
      type: 'warning',
    }
  )
  .then(() => {
    cartStore.clearCart();
    ElMessage.success('購物車已清空');
  })
  .catch(() => {
    // User cancelled
    ElMessage.info('已取消操作');
  });
};

const goToCheckout = () => {
  router.push('/checkout');
};

</script>

<style scoped>
.cart-page {
  padding: 20px;
}

.page-title {
  text-align: center;
  font-size: 2em;
  margin-bottom: 30px;
  color: #303133;
}

.cart-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.product-thumbnail {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 4px;
}

.cart-table {
  margin-bottom: 30px;
}

.cart-summary {
  padding: 20px;
  border: 1px solid #ebeef5; /* Element Plus divider color */
  border-radius: 4px;
  background-color: #f9fafc;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 1.1em;
  margin-bottom: 15px;
  color: #606266;
}

.summary-row:last-child {
  margin-bottom: 0;
}

.summary-value {
  font-weight: 600;
  color: #303133;
}

.total-price-row {
  font-size: 1.3em;
  border-top: 1px dashed #dcdfe6;
  padding-top: 15px;
}

.total-price {
  color: var(--el-color-danger);
}

.summary-actions {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

.summary-actions .el-button {
  margin-left: 15px;
}
</style> 