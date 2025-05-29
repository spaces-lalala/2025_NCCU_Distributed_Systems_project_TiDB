<template>
  <div class="checkout-page">
    <el-row :gutter="20">
      <!-- Left Side: Shipping Form & Payment -->
      <el-col :span="16">
        <el-card shadow="never" class="form-card">
          <template #header>
            <h2>填寫訂單資訊</h2>
          </template>
          <el-form
            ref="shippingFormRef"
            :model="shippingForm"
            :rules="shippingRules"
            label-position="top"
            @submit.prevent="handleSubmitOrder"
          >
            <el-divider content-position="left"><h3>收貨人資訊</h3></el-divider>
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="姓名" prop="name">
                  <el-input v-model="shippingForm.name" placeholder="收貨人姓名" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="連絡電話" prop="phone">
                  <el-input v-model="shippingForm.phone" placeholder="收貨人電話" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="收貨地址" prop="address">
              <el-input v-model="shippingForm.address" type="textarea" :rows="3" placeholder="詳細收貨地址" />
            </el-form-item>

            <el-divider content-position="left"><h3>配送與支付</h3></el-divider>
            <el-form-item label="配送方式" prop="shippingMethod">
              <el-radio-group v-model="shippingForm.shippingMethod">
                <el-radio value="standard">標準宅配</el-radio>
                <el-radio value="express">快速到貨 (費用 NT$ 100)</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="支付方式" prop="paymentMethod">
              <el-radio-group v-model="shippingForm.paymentMethod">
                <el-radio value="cod">貨到付款</el-radio>
                <el-radio value="credit_card_mock">信用卡 (模擬)</el-radio>
              </el-radio-group>
            </el-form-item>
            <el-form-item label="訂單備註 (可選)" prop="notes">
              <el-input v-model="shippingForm.notes" type="textarea" :rows="2" placeholder="如有特殊需求請在此註明" />
            </el-form-item>
          </el-form>
        </el-card>
      </el-col>

      <!-- Right Side: Order Summary & Submit Button -->
      <el-col :span="8">
        <el-card shadow="never" class="summary-card">
          <template #header>
            <h3>訂單摘要</h3>
          </template>
          <div v-if="!cartStore.isEmpty">
            <div v-for="item in cartStore.getCartItems" :key="item.id" class="summary-item">
              <span>{{ item.name }} x {{ item.quantity }}</span>
              <span>NT$ {{ (item.price * item.quantity).toFixed(2) }}</span>
            </div>
            <el-divider />
            <div class="summary-total">
              <span>商品總計:</span>
              <span>NT$ {{ cartStore.totalPrice.toFixed(2) }}</span>
            </div>
            <div class="summary-total" v-if="shippingForm.shippingMethod === 'express'">
              <span>運費:</span>
              <span>NT$ 100.00</span>
            </div>
            <el-divider />
            <div class="summary-grand-total">
              <strong>應付總額:</strong>
              <strong>NT$ {{ grandTotal.toFixed(2) }}</strong>
            </div>
            <el-button 
              type="danger" 
              @click="handleSubmitOrder" 
              class="submit-order-button" 
              :loading="isSubmitting"
              :disabled="cartStore.isEmpty">
              確認下單
            </el-button>
          </div>
          <el-empty v-else description="購物車是空的，無法結帳">
            <router-link to="/products"><el-button type="primary">繼續購物</el-button></router-link>
          </el-empty>
        </el-card>
      </el-col>
    </el-row>
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
  let total = cartStore.totalPrice;
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
.checkout-page {
  max-width: 1200px;
  margin: 20px auto;
  padding: 20px;
}

.form-card,
.summary-card {
  border: 1px solid #ebeef5;
  height: 100%; /* Make cards same height in the row */
}
.form-card h2,
.summary-card h3 {
  margin: 0;
  color: #303133;
}
.el-divider h3 {
  margin: 0;
  color: #606266;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 0;
  font-size: 0.9em;
}

.summary-total,
.summary-grand-total {
  display: flex;
  justify-content: space-between;
  padding: 10px 0;
  font-size: 1em;
}

.summary-grand-total strong {
  font-size: 1.2em;
  color: #f56c6c; /* Danger color for emphasis */
}

.submit-order-button {
  width: 100%;
  margin-top: 20px;
  padding: 12px 0; /* Larger button */
  font-size: 1.1em;
}

.el-form-item {
  margin-bottom: 18px; /* Adjust spacing */
}
</style> 