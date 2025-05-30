<template>
  <div class="checkout-page">
    <!-- Page Header -->
    <section class="page-header">
      <h1 class="page-title">結帳</h1>
      <p class="page-subtitle">完成您的訂單</p>
    </section>

    <div class="checkout-content">
      <el-row :gutter="32">
        <!-- Left Side: Shipping Form & Payment -->
        <el-col :lg="16" :md="24">
          <div class="form-section">
            <el-card shadow="never" class="form-card">
              <template #header>
                <div class="card-header">
                  <h2 class="card-title">訂單資訊</h2>
                  <p class="card-subtitle">請填寫收貨和付款資訊</p>
                </div>
              </template>
              <el-form
                ref="shippingFormRef"
                :model="shippingForm"
                :rules="shippingRules"
                label-position="top"
                @submit.prevent="handleSubmitOrder"
                class="checkout-form"
              >
                <div class="form-section-group">
                  <div class="section-header">
                    <h3 class="section-title">收貨人資訊</h3>
                  </div>
                  <el-row :gutter="20">
                    <el-col :span="12">
                      <el-form-item label="姓名" prop="name">
                        <el-input 
                          v-model="shippingForm.name" 
                          placeholder="請輸入收貨人姓名" 
                          size="large"
                        />
                      </el-form-item>
                    </el-col>
                    <el-col :span="12">
                      <el-form-item label="連絡電話" prop="phone">
                        <el-input 
                          v-model="shippingForm.phone" 
                          placeholder="請輸入聯絡電話" 
                          size="large"
                        />
                      </el-form-item>
                    </el-col>
                  </el-row>
                  <el-form-item label="收貨地址" prop="address">
                    <el-input 
                      v-model="shippingForm.address" 
                      type="textarea" 
                      :rows="3" 
                      placeholder="請輸入詳細收貨地址" 
                      size="large"
                    />
                  </el-form-item>
                </div>

                <div class="form-section-group">
                  <div class="section-header">
                    <h3 class="section-title">配送與支付</h3>
                  </div>
                  <el-form-item label="配送方式" prop="shippingMethod">
                    <el-radio-group v-model="shippingForm.shippingMethod" class="radio-group">
                      <el-radio value="standard" class="radio-option">
                        <div class="radio-content">
                          <span class="radio-title">標準宅配</span>
                          <span class="radio-description">免費配送，3-5個工作天</span>
                        </div>
                      </el-radio>
                      <el-radio value="express" class="radio-option">
                        <div class="radio-content">
                          <span class="radio-title">快速到貨</span>
                          <span class="radio-description">NT$ 100，1-2個工作天</span>
                        </div>
                      </el-radio>
                    </el-radio-group>
                  </el-form-item>
                  <el-form-item label="支付方式" prop="paymentMethod">
                    <el-radio-group v-model="shippingForm.paymentMethod" class="radio-group">
                      <el-radio value="cod" class="radio-option">
                        <div class="radio-content">
                          <span class="radio-title">貨到付款</span>
                          <span class="radio-description">收貨時現金付款</span>
                        </div>
                      </el-radio>
                      <el-radio value="credit_card_mock" class="radio-option">
                        <div class="radio-content">
                          <span class="radio-title">信用卡付款</span>
                          <span class="radio-description">模擬信用卡付款</span>
                        </div>
                      </el-radio>
                    </el-radio-group>
                  </el-form-item>
                  <el-form-item label="訂單備註" prop="notes">
                    <el-input 
                      v-model="shippingForm.notes" 
                      type="textarea" 
                      :rows="2" 
                      placeholder="如有特殊需求請在此註明（可選）" 
                      size="large"
                    />
                  </el-form-item>
                </div>
              </el-form>            </el-card>
          </div>
        </el-col>
        
        <!-- Right Side: Order Summary & Submit Button -->
        <el-col :lg="8" :md="24">
          <div class="summary-section">
            <el-card shadow="never" class="summary-card">
              <template #header>
                <div class="card-header">
                  <h3 class="card-title">訂單摘要</h3>
                  <p class="card-subtitle">檢查您的訂單</p>
                </div>
              </template>
              <div v-if="!cartStore.isEmpty">
                <div class="order-items">
                  <div v-for="item in cartStore.getCartItems" :key="item.id" class="order-item">
                    <div class="item-info">
                      <span class="item-name">{{ item.name }}</span>
                      <span class="item-quantity">x {{ item.quantity }}</span>
                    </div>
                    <span class="item-total">NT$ {{ ((item.price || 0) * item.quantity).toFixed(2) }}</span>
                  </div>
                </div>
                  <div class="summary-calculations">
                  <div class="summary-row">
                    <span class="label">商品總計</span>
                    <span class="value">NT$ {{ cartStore.getTotalPrice.toFixed(2) }}</span>
                  </div>
                  <div class="summary-row" v-if="shippingForm.shippingMethod === 'express'">
                    <span class="label">運費</span>
                    <span class="value">NT$ 100.00</span>
                  </div>
                  <div class="summary-row" v-else>
                    <span class="label">運費</span>
                    <span class="value free">免費</span>
                  </div>
                  <div class="summary-divider"></div>
                  <div class="summary-row total-row">
                    <span class="label">應付總額</span>
                    <span class="value">NT$ {{ grandTotal.toFixed(2) }}</span>
                  </div>
                </div>
                
                <div class="submit-section">
                  <el-button 
                    type="primary" 
                    size="large"
                    @click="handleSubmitOrder" 
                    class="submit-order-button" 
                    :loading="isSubmitting"
                    :disabled="cartStore.isEmpty"
                  >
                    <span v-if="!isSubmitting">確認下單</span>
                    <span v-else>處理中...</span>
                  </el-button>
                </div>
              </div>
              <div v-else class="empty-cart">
                <el-empty :image-size="100" description="購物車是空的">
                  <template #description>
                    <p class="empty-text">無法結帳，請先添加商品</p>
                  </template>
                  <router-link to="/products">
                    <el-button type="primary" size="large">繼續購物</el-button>
                  </router-link>
                </el-empty>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue';
import { useCartStore } from '@/store/cart';
import { useAuthStore } from '@/store/auth';
import { useRouter } from 'vue-router';
import { ElMessage, ElMessageBox, ElForm, ElFormItem, ElInput, ElRadioGroup, ElRadio, ElButton, ElCard, ElRow, ElCol, ElDivider, ElEmpty } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus';
import { createOrder } from '@/services/orderService';
import type { OrderCreationPayload, Order, OrderItemForCreation } from '@/types/order';

const cartStore = useCartStore();
const authStore = useAuthStore();
const router = useRouter();

const shippingFormRef = ref<FormInstance>();
const isSubmitting = ref(false);

interface ShippingFormData {
  name: string;
  phone: string;
  address: string;
  shippingMethod: 'standard' | 'express';
  paymentMethod: 'cod' | 'credit_card_mock';
  notes?: string;
}

const shippingForm = reactive<ShippingFormData> ({
  name: authStore.user?.name || '', // Pre-fill if user is logged in
  phone: '',
  address: '',
  shippingMethod: 'standard',
  paymentMethod: 'cod',
  notes: '',
});

const shippingRules = reactive<FormRules> ({
  name: [{ required: true, message: '請輸入收貨人姓名', trigger: 'blur' }],
  phone: [{ required: true, message: '請輸入連絡電話', trigger: 'blur' }],
  address: [{ required: true, message: '請輸入收貨地址', trigger: 'blur' }],
  shippingMethod: [{ required: true, message: '請選擇配送方式', trigger: 'change' }],
  paymentMethod: [{ required: true, message: '請選擇支付方式', trigger: 'change' }],
});

const grandTotal = computed(() => {
  let total = cartStore.getTotalPrice;
  if (shippingForm.shippingMethod === 'express') {
    total += 100; // Add shipping fee for express
  }
  return total;
});

const handleSubmitOrder = async () => {
  if (!shippingFormRef.value) return;
  if (cartStore.isEmpty) {
    ElMessage.warning('您的購物車是空的，無法提交訂單。');
    return;
  }

  await shippingFormRef.value.validate(async (valid) => {
    if (valid) {
      isSubmitting.value = true;
      try {
        // 最終庫存驗證 - 確保在提交訂單前所有商品都有足夠庫存
        ElMessage.info('正在進行最終庫存驗證...');
        const validation = await cartStore.validateCartStock();
        
        if (!validation.valid) {
          ElMessage.error('庫存驗證失敗，無法提交訂單');
          ElMessageBox.alert(
            validation.issues.join('\n'),
            '庫存不足',
            {
              confirmButtonText: '返回購物車調整',
              type: 'warning',
            }
          ).then(() => {
            router.push('/cart');
          });
          return;
        }

        const itemsForApi: OrderItemForCreation[] = cartStore.getCartItems.map(item => ({
          product_id: parseInt(item.id),  // Backend expects product_id as integer
          quantity: item.quantity
        }));

        const payloadForApi: OrderCreationPayload = {
          items: itemsForApi
        };        const createdOrder: Order = await createOrder(payloadForApi);

        ElMessage.success(`訂單已成功提交！訂單編號: ${createdOrder.order_number}`);
        cartStore.clearCart();
        router.push({
          name: 'OrderConfirmation',
          params: { 
            orderId: createdOrder.id,
            orderNumber: createdOrder.order_number
          }
        });

      } catch (error: any) {
        // 特別處理認證錯誤
        if (error.message && error.message.includes('Could not validate credentials')) {
          ElMessage.error('登入已過期，請重新登入後再試');
          // 清除認證資訊並重定向到登入頁面
          localStorage.removeItem('authToken');
          localStorage.removeItem('authUser');
          router.push('/login');
        } else {
          ElMessage.error(error.message || '訂單提交失敗，請稍後再試。');
        }
        console.error('Order submission error:', error);
      } finally {
        isSubmitting.value = false;
      }
    } else {
      ElMessage.error('表單資料有誤，請檢查後再提交。');
    }
  });
};

onMounted(() => {
  if (cartStore.isEmpty) {
    // Optionally redirect if cart is empty when page loads, though user might be coming back
    // ElMessage.info('您的購物車是空的，正在導向商品頁...');
    // router.push('/products');
  }
  // Pre-fill name from authStore if available and form name is empty
  if (authStore.user?.name && !shippingForm.name) {
    shippingForm.name = authStore.user.name;
  }
});
</script>

<style scoped>
/* Page Structure */
.checkout-page {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: var(--spacing-lg);
  background: var(--background-color);
  min-height: 100vh;
}

/* Page Header */
.page-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-md);
  border-bottom: 1px solid var(--border-color);
}

.page-title {
  font-size: var(--font-size-xxl);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0 0 var(--spacing-sm) 0;
}

.page-subtitle {
  font-size: var(--font-size-md);
  color: var(--text-secondary);
  margin: 0;
}

/* Layout */
.checkout-content {
  margin-top: var(--spacing-xl);
}

/* Form Section */
.form-section {
  margin-bottom: var(--spacing-lg);
}

.form-card,
.summary-card {
  border: 1px solid var(--border-color);
  border-radius: var(--border-radius-md);
  box-shadow: var(--shadow-sm);
  background: var(--surface-color);
  height: 100%;
}

.form-card :deep(.el-card__header),
.summary-card :deep(.el-card__header) {
  padding: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  background: var(--surface-color);
}

.form-card :deep(.el-card__body),
.summary-card :deep(.el-card__body) {
  padding: var(--spacing-lg);
}

/* Card Headers */
.card-header {
  text-align: left;
}

.card-title {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0 0 var(--spacing-xs) 0;
}

.card-subtitle {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: 0;
}

/* Form Styling */
.checkout-form {
  margin-top: var(--spacing-md);
}

.form-section-group {
  margin-bottom: var(--spacing-xl);
  padding: var(--spacing-lg);
  background: var(--background-light);
  border-radius: var(--border-radius);
  border: 1px solid var(--border-light);
}

.section-header {
  margin-bottom: var(--spacing-md);
  padding-bottom: var(--spacing-sm);
  border-bottom: 1px solid var(--border-color);
}

.section-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0;
}

/* Form Elements */
.checkout-form :deep(.el-form-item) {
  margin-bottom: var(--spacing-lg);
}

.checkout-form :deep(.el-form-item__label) {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
  margin-bottom: var(--spacing-xs);
}

.checkout-form :deep(.el-input__wrapper) {
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
  box-shadow: none;
  transition: var(--transition-base);
}

.checkout-form :deep(.el-input__wrapper:hover) {
  border-color: var(--primary-color);
}

.checkout-form :deep(.el-textarea__inner) {
  border-radius: var(--border-radius);
  border: 1px solid var(--border-color);
  font-family: inherit;
}

/* Radio Group Styling */
.radio-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  width: 100%;
}

.radio-option {
  padding: var(--spacing-lg);
  border: 2px solid var(--border-color);
  border-radius: var(--border-radius);
  background: var(--surface-color);
  transition: var(--transition-base);
  margin: 0;
  width: 100%;
  display: block;
  position: relative;
  min-height: 80px;
  box-sizing: border-box;
}

.radio-option :deep(.el-radio__input) {
  position: absolute;
  top: var(--spacing-md);
  left: var(--spacing-md);
  z-index: 1;
}

.radio-option :deep(.el-radio__label) {
  padding-left: calc(var(--spacing-md) + 24px);
  display: block;
  width: calc(100% - var(--spacing-md) - 24px);
  box-sizing: border-box;
  line-height: 1.5;
  overflow: visible;
}

.radio-option:hover {
  border-color: var(--primary-color);
  background: var(--primary-light);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.radio-option:deep(.el-radio.is-checked) {
  border-color: var(--primary-color);
  background: var(--primary-light);
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.2);
}

.radio-content {
  display: flex;
  flex-direction: column;
  gap: 6px;
  width: 100%;
  box-sizing: border-box;
  min-height: 48px;
  justify-content: center;
}

.radio-title {
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  font-size: var(--font-size-base);
  line-height: 1.5;
  margin: 0;
  white-space: normal;
  word-break: break-word;
  overflow-wrap: break-word;
}

.radio-description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  line-height: 1.4;
  margin: 0;
  white-space: normal;
  word-break: break-word;
  overflow-wrap: break-word;
}

/* Summary Section */
.summary-section {
  position: sticky;
  top: var(--spacing-lg);
}

.order-items {
  margin-bottom: var(--spacing-lg);
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid var(--border-light);
}

.order-item:last-child {
  border-bottom: none;
}

.item-info {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
  flex: 1;
}

.item-name {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

.item-quantity {
  font-size: var(--font-size-xs);
  color: var(--text-secondary);
}

.item-total {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

/* Summary Calculations */
.summary-calculations {
  margin-top: var(--spacing-lg);
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-sm) 0;
}

.summary-row .label {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
}

.summary-row .value {
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  font-size: var(--font-size-sm);
}

.summary-row .value.free {
  color: var(--success-color);
}

.summary-divider {
  height: 1px;
  background: var(--border-color);
  margin: var(--spacing-md) 0;
}

.total-row {
  padding: var(--spacing-md) 0;
  border-top: 2px solid var(--border-color);
  margin-top: var(--spacing-sm);
}

.total-row .label {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
}

.total-row .value {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
}

/* Submit Section */
.submit-section {
  margin-top: var(--spacing-xl);
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-color);
}

.submit-order-button {
  width: 100%;
  height: 48px;
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  border-radius: var(--border-radius);
  transition: all 0.3s ease;
}

/* 使用更強的選擇器來確保樣式優先級 */
.checkout-page .submit-section .submit-order-button.el-button.el-button--primary {
  background-color: #409eff !important;
  border-color: #409eff !important;
  color: #ffffff !important;
}

.checkout-page .submit-section .submit-order-button.el-button.el-button--primary:hover:not(.is-disabled):not(:disabled) {
  background-color: #337ecc !important;
  border-color: #337ecc !important;
  color: #ffffff !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.3);
}

.checkout-page .submit-section .submit-order-button.el-button.el-button--primary:active:not(.is-disabled):not(:disabled) {
  background-color: #2b6cb0 !important;
  border-color: #2b6cb0 !important;
  color: #ffffff !important;
  transform: translateY(0);
}

.checkout-page .submit-section .submit-order-button.el-button.el-button--primary:focus:not(.is-disabled):not(:disabled) {
  background-color: #409eff !important;
  border-color: #409eff !important;
  color: #ffffff !important;
  box-shadow: 0 0 0 2px rgba(64, 158, 255, 0.2);
}

.checkout-page .submit-section .submit-order-button.el-button.el-button--primary.is-disabled,
.checkout-page .submit-section .submit-order-button.el-button.el-button--primary:disabled {
  opacity: 0.6 !important;
  cursor: not-allowed !important;
  transform: none !important;
  box-shadow: none !important;
  background-color: #cccccc !important;
  border-color: #cccccc !important;
  color: #666666 !important;
}

.checkout-page .submit-section .submit-order-button.el-button.el-button--primary.is-loading {
  background-color: #409eff !important;
  border-color: #409eff !important;
  color: #ffffff !important;
}

/* Empty State */
.empty-cart {
  text-align: center;
  padding: var(--spacing-xl);
}

.empty-text {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
  margin: var(--spacing-md) 0;
}

/* Responsive Design */
@media (max-width: 768px) {
  .checkout-page {
    padding: var(--spacing-md);
  }
  
  .checkout-content :deep(.el-col) {
    margin-bottom: var(--spacing-lg);
  }
  
  .form-section-group {
    padding: var(--spacing-md);
  }
  
  .radio-option {
    padding: var(--spacing-md);
    min-height: 75px;
  }
  
  .radio-option :deep(.el-radio__label) {
    padding-left: calc(var(--spacing-sm) + 20px);
    width: calc(100% - var(--spacing-sm) - 20px);
  }
  
  .radio-content {
    gap: 4px;
    min-height: 40px;
  }
  
  .radio-title {
    font-size: var(--font-size-sm);
    line-height: 1.4;
  }
  
  .radio-description {
    font-size: var(--font-size-xs);
    line-height: 1.3;
  }
  
  .submit-order-button {
    height: 44px;
    font-size: var(--font-size-sm);
  }
}

@media (max-width: 480px) {
  .checkout-page {
    padding: var(--spacing-sm);
  }
  
  .page-title {
    font-size: var(--font-size-xl);
  }
  
  .form-section-group {
    padding: var(--spacing-sm);
  }
  
  .radio-option {
    padding: var(--spacing-sm);
    min-height: 70px;
  }
  
  .radio-option :deep(.el-radio__label) {
    padding-left: calc(var(--spacing-xs) + 18px);
    width: calc(100% - var(--spacing-xs) - 18px);
  }
  
  .radio-content {
    gap: 3px;
    min-height: 36px;
  }
  
  .radio-title {
    font-size: var(--font-size-xs);
    line-height: 1.3;
  }
  
  .radio-description {
    font-size: 10px;
    line-height: 1.2;
  }
  
  .submit-order-button {
    height: 40px;
    font-size: var(--font-size-sm);
  }
}
</style>