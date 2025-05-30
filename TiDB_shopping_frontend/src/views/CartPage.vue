<template>
  <div class="cart-page">
    <!-- Page Header -->
    <section class="page-header">
      <h1 class="page-title">購物車</h1>
      <p class="page-subtitle">檢視您選購的商品</p>
    </section>

    <!-- Empty Cart State -->
    <section v-if="cartStore.isEmpty" class="empty-cart-section">
      <el-empty description="您的購物車目前是空的" :image-size="120">
        <template #description>
          <p class="empty-description">快去挑選您喜歡的商品吧！</p>
        </template>
        <router-link to="/products">
          <el-button type="primary" size="large" class="shop-button">
            前往購物
          </el-button>
        </router-link>
      </el-empty>
    </section>

    <!-- Cart Content -->
    <section v-else class="cart-content">
      <!-- Cart Items -->
      <div class="cart-items-section">
        <div class="section-title">商品清單</div>
        
        <div class="cart-items-container">
          <div 
            v-for="item in cartStore.getCartItems" 
            :key="item.id"
            class="cart-item"
          >
            <div class="item-image">
              <img :src="item.imageUrl" :alt="item.name" />
            </div>
            
            <div class="item-info">
              <h4 class="item-name">{{ item.name }}</h4>
              <div class="item-price">NT$ {{ (item.price || 0).toFixed(2) }}</div>
            </div>
            
            <div class="item-quantity">
              <label class="quantity-label">數量</label>
              <el-input-number
                :model-value="item.quantity"
                @change="(currentValue) => handleQuantityChange(item.id, currentValue)"
                :min="1"
                :max="item.stock" 
                size="default"
                controls-position="right"
              />
            </div>
            
            <div class="item-subtotal">
              <div class="subtotal-label">小計</div>
              <div class="subtotal-amount">NT$ {{ ((item.price || 0) * item.quantity).toFixed(2) }}</div>
            </div>
            
            <div class="item-actions">
              <el-button 
                type="danger" 
                :icon="Delete" 
                circle 
                plain 
                @click="confirmRemoveItem(item.id)" 
                class="remove-button"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- Cart Summary -->
      <div class="cart-summary-section">
        <div class="summary-card">
          <div class="summary-header">
            <h3>訂單總計</h3>
          </div>
          
          <div class="summary-details">
            <div class="summary-row">
              <span>商品總額</span>
              <span>NT$ {{ cartStore.getTotalPrice.toFixed(2) }}</span>
            </div>
            <div class="summary-row">
              <span>運費</span>
              <span>免費</span>
            </div>
            <div class="summary-divider"></div>
            <div class="summary-row total-row">
              <span>總計</span>
              <span>NT$ {{ cartStore.getTotalPrice.toFixed(2) }}</span>
            </div>
          </div>
          
          <div class="summary-actions">
            <el-button 
              @click="clearCart" 
              plain 
              class="clear-button"
            >
              清空購物車
            </el-button>
            <router-link to="/checkout">
              <el-button 
                type="primary" 
                size="large" 
                class="checkout-button"
              >
                前往結帳
              </el-button>
            </router-link>
          </div>
        </div>
      </div>    </section>
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

const handleQuantityChange = async (productId: string | number, newQuantity: number | undefined) => {
  if (newQuantity === undefined || newQuantity < 1) {
    // If undefined or less than 1, treat as attempt to remove or invalid input, 
    // consider prompting to remove or setting to 1.
    // For now, we rely on el-input-number's min prop for direct input.
    // If the change event fires with undefined, it might mean the field was cleared.
    // We might want to remove the item or set quantity to 1.
    // For simplicity, if newQuantity is undefined, we can re-fetch the current quantity or set to 1
    const item = cartStore.getCartItems.find(i => i.id == productId); // 使用 == 來比較不同類型
    if (item) cartStore.updateItemQuantity(productId, item.quantity); // revert or set to 1
    return;
  }

  // 使用新的庫存驗證方法
  const success = await cartStore.updateItemQuantity(productId, newQuantity);
  if (success) {
    ElMessage.success('購物車數量已更新');
  } else {
    // 獲取最新庫存並顯示錯誤訊息
    const currentStock = await cartStore.checkProductStock(productId);
    if (currentStock === null) {
      ElMessage.error('無法驗證庫存，請稍後再試');
    } else if (currentStock <= 0) {
      ElMessage.error('商品已售完，將從購物車中移除');
      cartStore.removeItem(productId);
    } else {
      ElMessage.warning(`庫存不足，目前僅剩 ${currentStock} 件，已調整至最大可購買數量`);
      // 將數量調整為庫存數量
      await cartStore.updateItemQuantity(productId, currentStock);
    }
  }
};

const confirmRemoveItem = (productId: string | number) => {
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

const goToCheckout = async () => {
  // For now, just a placeholder. Later, this will navigate to the checkout page.
  if (cartStore.isEmpty) {
    ElMessage.warning('您的購物車是空的，請先加入商品再結帳。');
    return;
  }

  // 結帳前驗證整個購物車的庫存
  ElMessage.info('正在驗證商品庫存...');
  const validation = await cartStore.validateCartStock();
  
  if (!validation.valid) {
    ElMessageBox.alert(
      validation.issues.join('\n'),
      '庫存不足，無法結帳',
      {
        confirmButtonText: '確定',
        type: 'warning',
      }
    );
    return;
  }

  ElMessage.success('庫存驗證通過，前往結帳頁面');
  router.push('/checkout'); // Navigate to checkout page
};

</script>

<style scoped>
.cart-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

/* Page Header */
.page-header {
  text-align: center;
}

.page-title {
  font-size: var(--font-size-xxxl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.page-subtitle {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  margin-bottom: 0;
}

/* Empty Cart Section */
.empty-cart-section {
  background-color: var(--bg-color);
  border-radius: var(--border-radius-large);
  padding: var(--spacing-xxxl);
  text-align: center;
  box-shadow: var(--shadow-light);
}

.empty-description {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-lg);
}

.shop-button {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-lg);
  font-weight: 600;
}

/* Cart Content */
.cart-content {
  display: grid;
  grid-template-columns: 1fr 350px;
  gap: var(--spacing-xl);
  align-items: start;
}

/* Cart Items Section */
.cart-items-section {
  background-color: var(--bg-color);
  border-radius: var(--border-radius-large);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-light);
}

.section-title {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
  border-bottom: 2px solid var(--border-lighter);
  padding-bottom: var(--spacing-md);
}

.cart-items-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Cart Item */
.cart-item {
  display: grid;
  grid-template-columns: 80px 1fr auto auto auto;
  gap: var(--spacing-lg);
  align-items: center;
  padding: var(--spacing-lg);
  background-color: var(--bg-page);
  border-radius: var(--border-radius-base);
  border: 1px solid var(--border-lighter);
  transition: all 0.3s ease;
}

.cart-item:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-base);
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: var(--border-radius-base);
  overflow: hidden;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.item-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.item-price {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  font-weight: 500;
}

.item-quantity {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  align-items: center;
}

.quantity-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  font-weight: 500;
}

.item-subtotal {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  align-items: center;
  text-align: center;
}

.subtotal-label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  font-weight: 500;
}

.subtotal-amount {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--primary-color);
}

.item-actions {
  display: flex;
  justify-content: center;
}

.remove-button {
  padding: var(--spacing-sm);
}

/* Cart Summary Section */
.cart-summary-section {
  position: sticky;
  top: var(--spacing-xl);
}

.summary-card {
  background-color: var(--bg-color);
  border-radius: var(--border-radius-large);
  padding: var(--spacing-xl);
  box-shadow: var(--shadow-base);
  border: 1px solid var(--border-lighter);
}

.summary-header {
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-md);
  border-bottom: 2px solid var(--border-lighter);
}

.summary-header h3 {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--text-primary);
  margin: 0;
}

.summary-details {
  margin-bottom: var(--spacing-lg);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
  font-size: var(--font-size-base);
}

.summary-row span:first-child {
  color: var(--text-secondary);
}

.summary-row span:last-child {
  font-weight: 500;
  color: var(--text-primary);
}

.summary-divider {
  height: 1px;
  background-color: var(--border-lighter);
  margin: var(--spacing-md) 0;
}

.total-row {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
}

.total-row span:last-child {
  color: var(--primary-color);
  font-size: var(--font-size-xl);
}

.summary-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.clear-button,
.checkout-button {
  width: 100%;
  padding: var(--spacing-md);
  font-size: var(--font-size-base);
  font-weight: 600;
}

.checkout-button {
  font-size: var(--font-size-lg);
}

/* Responsive Design */
@media (max-width: 1024px) {
  .cart-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
  }
  
  .cart-summary-section {
    position: static;
  }
}

@media (max-width: 768px) {
  .cart-item {
    grid-template-columns: 60px 1fr;
    grid-template-rows: auto auto auto;
    gap: var(--spacing-md);
    padding: var(--spacing-md);
  }
  
  .item-image {
    width: 60px;
    height: 60px;
  }
  
  .item-info {
    grid-column: 2;
  }
  
  .item-quantity,
  .item-subtotal,
  .item-actions {
    grid-column: 1 / -1;
    justify-self: stretch;
  }
  
  .item-quantity,
  .item-subtotal {
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
  }
  
  .item-actions {
    justify-content: center;
  }
  
  .page-title {
    font-size: var(--font-size-xxl);
  }
}

@media (max-width: 576px) {
  .page-title {
    font-size: var(--font-size-xl);
  }
  
  .cart-item {
    padding: var(--spacing-sm);
  }
  
  .summary-card {
    padding: var(--spacing-lg);
  }
}
</style>