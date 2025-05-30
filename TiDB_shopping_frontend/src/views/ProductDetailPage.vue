<template>
  <div class="product-detail-page">
    <div v-if="product" class="product-content">
      <div class="product-image-section">
        <div class="product-image-container">
          <img :src="product.imageUrl" :alt="product.name" class="product-image" />
        </div>
      </div>
      
      <div class="product-info-section">
        <div class="product-header">
          <h1 class="product-title">{{ product.name }}</h1>
          <p class="product-description">{{ product.description }}</p>
        </div>
          <div class="product-pricing">
          <div class="price-container">
            <span class="price-label">價格</span>
            <span class="price-value">NT$ {{ (product.price || 0).toFixed(2) }}</span>
          </div>
          
          <div class="stock-container">
            <span class="stock-label">庫存</span>
            <span class="stock-value" :class="{ 'out-of-stock': product.stock <= 0, 'low-stock': product.stock > 0 && product.stock <= 5 }">
              {{ product.stock <= 0 ? '已售完' : `${product.stock} 件` }}
            </span>
          </div>
        </div>
        
        <div class="product-actions">
          <div class="quantity-section">
            <label for="quantity" class="quantity-label">數量</label>
            <el-input-number
              id="quantity"
              v-model="quantity"
              :min="product.stock > 0 ? 1 : 0"
              :max="Math.max(1, product.stock)"
              :disabled="product.stock <= 0"
              controls-position="right"
              class="quantity-input"
            />
          </div>
          <el-button 
            type="primary" 
            size="large" 
            @click="addToCart" 
            class="add-to-cart-button"
            :disabled="product.stock <= 0"
            :loading="false"
          >
            {{ product.stock <= 0 ? '已售完' : '加入購物車' }}
          </el-button>
        </div>
      </div>
    </div>
    
    <div v-else-if="isLoading" class="loading-section">
      <el-skeleton :rows="5" animated />
      <div class="loading-text">載入商品資訊中...</div>
    </div>
    
    <div v-else class="not-found-section">
      <el-empty :image-size="200" description="">
        <template #description>
          <h2 class="not-found-title">商品未找到</h2>
          <p class="not-found-text">抱歉，我們找不到您要查找的商品。</p>
        </template>
        <router-link to="/products">
          <el-button type="primary" size="large">
            返回商品列表
          </el-button>
        </router-link>
      </el-empty>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Product } from '@/types/product';
import { useCartStore } from '@/store/cart';
import { ElMessage, ElButton, ElInputNumber, ElSkeleton, ElEmpty } from 'element-plus';

import { productImageMap } from '@/assets/images/ProductImageMaps';

const route = useRoute();
const router = useRouter(); // Optional: for navigation if needed

const product = ref<Product | null>(null);
const quantity = ref<number>(1);
const isLoading = ref<boolean>(true);
const cartStore = useCartStore();




// const fetchProductDetails = async () => {
//   isLoading.value = true;
//   const productId = route.params.id as string;

//   try {
//     const response = await fetch(`/api/products/${productId}`);//後端的路徑
//     if (!response.ok) throw new Error('Fetch failed');

//     const stockData = await res.json();

//     const mock = mockProducts.find(p => p.id === productId);
//     if (!mock) throw new Error('找不到 mock 商品');

//     const finalProduct = {
//       ...mock,
//       stock: stockData.stock,
//       price: stockData.stock < 500 ? mock.price + 10 : mock.price
//     };

//     product.value = finalProduct;
//   } catch (error) {
//     console.error('商品讀取失敗：', error);
//     product.value = null;
//   } finally {
//     isLoading.value = false;
//   }
// };

const fetchProductDetails = async () => {
  isLoading.value = true;
  const productId = route.params.id as string;

  try {
    const response = await fetch(`/api/products/${productId}`);
    
    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('商品未找到');
      }
      throw new Error(`載入失敗: ${response.status}`);
    }

    const data = await response.json();
    console.log('API Response:', data); // Debug log
    
    // 確保數據格式正確
    if (!data.id || !data.name || data.price === undefined) {
      throw new Error('商品數據格式錯誤');
    }

    // 轉換數據格式以符合前端期望
    product.value = {
      id: data.id,
      name: data.name,      description: data.description || '暫無商品描述',
      price: Number(data.price),
      stock: Number(data.stock || 0),
      imageUrl: productImageMap[data.name] ?? data.image_url ?? '',
      image_url: data.image_url,
      sold: data.sold,
      category_name: data.category_name
    };
    
    // 重置數量選擇器，確保不會違反 min/max 約束
    // 當庫存為 0 時，數量設為 0；有庫存時設為 1
    quantity.value = product.value.stock > 0 ? 1 : 0;
    
  } catch (error) {
    console.error('商品讀取失敗：', error);
    product.value = null;
    ElMessage.error(error instanceof Error ? error.message : '載入商品失敗，請稍後再試');
  } finally {
    isLoading.value = false;
  }
};


const addToCart = async () => {
  if (!product.value) {
    ElMessage.error('商品資料載入中，請稍後再試');
    return;
  }

  if (quantity.value < 1) {
    ElMessage.warning('商品數量至少為 1');
    quantity.value = 1;
    return;
  }

  if (product.value.stock <= 0) {
    ElMessage.error('商品已售完，無法加入購物車');
    return;
  }

  if (quantity.value > product.value.stock) {
    ElMessage.warning(`庫存不足，目前僅剩 ${product.value.stock} 件`);
    quantity.value = product.value.stock;
    return;
  }

  try {
    // 使用新的 addItem 方法，它會自動處理庫存檢查和商品合併
    const result = await cartStore.addItem(product.value, quantity.value);
    
    if (result.success) {
      ElMessage.success(result.message);
      // 重置數量選擇器，確保不會違反約束
      quantity.value = 1;
    } else {
      ElMessage.warning(result.message);
      // 如果是庫存不足的錯誤，可以嘗試調整數量
      if (result.message.includes('最多還可加入')) {
        const match = result.message.match(/最多還可加入 (\d+) 件/);
        if (match) {
          const maxAddable = parseInt(match[1]);
          quantity.value = Math.max(1, maxAddable);
        }
      }
    }
  } catch (error) {
    console.error('加入購物車失敗：', error);
    ElMessage.error('加入購物車失敗，請稍後再試');
  }
};

onMounted(() => {
  fetchProductDetails();
});

// 監聽路由變化，當用戶從一個商品詳情頁導航到另一個商品詳情頁時重新載入
watch(() => route.params.id, (newId) => {
  if (newId) {
    fetchProductDetails();
  }
});

</script>

<style scoped>
.product-detail-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-lg) var(--spacing-md);
}

/* Product Content */
.product-content {
  display: grid;
  grid-template-columns: 45% 55%;
  gap: var(--spacing-xxl);
  background-color: var(--bg-color);
  border-radius: var(--border-radius-large);
  padding: var(--spacing-xxl);
  box-shadow: var(--shadow-base);
  margin-bottom: var(--spacing-xl);
  border: 1px solid var(--border-lighter);
}

/* Product Image Section */
.product-image-section {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: var(--spacing-lg);
}

.product-image-container {
  width: 100%;
  max-width: 400px;
  border-radius: var(--border-radius-large);
  overflow: hidden;
  background-color: var(--bg-page);
  border: 2px solid var(--border-lighter);
  box-shadow: var(--shadow-light);
  transition: all 0.3s ease;
}

.product-image-container:hover {
  border-color: var(--primary-color);
  box-shadow: var(--shadow-base);
}

.product-image {
  width: 100%;
  height: auto;
  aspect-ratio: 1;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.product-image:hover {
  transform: scale(1.02);
}

/* Product Info Section */
.product-info-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  padding: var(--spacing-md);
}

.product-header {
  border-bottom: 2px solid var(--border-lighter);
  padding-bottom: var(--spacing-lg);
  margin-bottom: var(--spacing-md);
}

.product-title {
  font-size: var(--font-size-xxxl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
  line-height: 1.3;
  letter-spacing: -0.02em;
}

.product-description {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  line-height: 1.6;
  margin: 0;
  padding: var(--spacing-sm) 0;
}

/* Product Pricing */
.product-pricing {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--spacing-md);
  margin: var(--spacing-lg) 0;
}

.price-container,
.stock-container {
  padding: var(--spacing-lg) var(--spacing-md);
  background: linear-gradient(135deg, var(--bg-page) 0%, rgba(255, 255, 255, 0.8) 100%);
  border-radius: var(--border-radius-base);
  border: 1px solid var(--border-lighter);
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.price-container::before,
.stock-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
}

.price-container:hover,
.stock-container:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-base);
}

.price-label,
.stock-label {
  display: block;
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
  text-transform: uppercase;
  letter-spacing: 0.8px;
}

.price-value {
  font-size: var(--font-size-xxl);
  font-weight: 700;
  color: var(--primary-color);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.stock-value {
  font-size: var(--font-size-xl);
  font-weight: 600;
  color: var(--success-color);
}

.stock-value.low-stock {
  color: var(--warning-color);
}

.stock-value.out-of-stock {
  color: var(--danger-color);
}

/* Product Actions */
.product-actions {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  padding: var(--spacing-lg);
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, var(--bg-page) 100%);
  border-radius: var(--border-radius-base);
  border: 1px solid var(--border-lighter);
  margin-top: var(--spacing-md);
}

.quantity-section {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.quantity-label {
  font-size: var(--font-size-base);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-xs);
}

.quantity-input {
  width: 100%;
  max-width: 160px;
}

.add-to-cart-button {
  width: 100%;
  padding: var(--spacing-lg);
  font-size: var(--font-size-lg);
  font-weight: 600;
  border-radius: var(--border-radius-base);
  transition: all 0.3s ease;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  border: none;
  box-shadow: var(--shadow-base);
}

.add-to-cart-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-dark);
}

.add-to-cart-button:disabled {
  background: var(--text-disabled);
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.stock-value.out-of-stock {
  color: var(--danger-color);
}

/* Loading Section */
.loading-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-lg) var(--spacing-md);
  background-color: var(--bg-color);
  border-radius: var(--border-radius-large);
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-lighter);
}

.loading-text {
  text-align: center;
  margin-top: var(--spacing-lg);
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  font-weight: 500;
}

/* Not Found Section */
.not-found-section {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-lg) var(--spacing-md);
  background-color: var(--bg-color);
  border-radius: var(--border-radius-large);
  text-align: center;
  box-shadow: var(--shadow-light);
  border: 1px solid var(--border-lighter);
}

.not-found-title {
  font-size: var(--font-size-xxl);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.not-found-text {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-xl);
  line-height: 1.6;
}

/* Responsive Design */
@media (max-width: 1024px) {
  .product-detail-page {
    padding: var(--spacing-md) var(--spacing-sm);
  }
  
  .product-content {
    grid-template-columns: 1fr;
    gap: var(--spacing-lg);
    padding: var(--spacing-lg);
  }
  
  .product-image-container {
    max-width: 350px;
    margin: 0 auto;
  }
}

@media (max-width: 768px) {
  .product-detail-page {
    padding: var(--spacing-sm);
  }
  
  .product-content {
    padding: var(--spacing-md);
    gap: var(--spacing-md);
  }
  
  .product-title {
    font-size: var(--font-size-xxl);
  }
  
  .product-pricing {
    grid-template-columns: 1fr;
    gap: var(--spacing-sm);
  }
  
  .quantity-section {
    flex-direction: column;
    align-items: stretch;
    gap: var(--spacing-sm);
  }
  
  .quantity-label {
    text-align: left;
  }
  
  .quantity-input {
    max-width: 100%;
  }
  
  .product-image-container {
    max-width: 280px;
  }
}

@media (max-width: 576px) {
  .product-content {
    padding: var(--spacing-sm);
  }
  
  .product-title {
    font-size: var(--font-size-xl);
  }
  
  .price-container,
  .stock-container {
    padding: var(--spacing-md) var(--spacing-sm);
  }
  
  .price-value {
    font-size: var(--font-size-xl);
  }
  
  .stock-value {
    font-size: var(--font-size-lg);
  }
  
  .product-actions {
    padding: var(--spacing-md);
  }
    .add-to-cart-button {
    padding: var(--spacing-md);
    font-size: var(--font-size-base);
  }
  
  .product-title {
    font-size: var(--font-size-xl);
  }
  
  .price-container,
  .stock-container {
    padding: var(--spacing-md);
  }
  
  .price-value {
    font-size: var(--font-size-xl);
  }
  
  .stock-value {
    font-size: var(--font-size-lg);
  }
}
</style>