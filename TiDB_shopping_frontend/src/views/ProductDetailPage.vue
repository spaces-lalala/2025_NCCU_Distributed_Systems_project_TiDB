<template>
  <div class="product-detail-page">
    <div v-if="product" class="product-content">
      <div class="product-image-container">
        <img :src="product.imageUrl" :alt="product.name" class="product-image" />
      </div>
      <div class="product-info">
        <h1>{{ product.name }}</h1>
        <p class="product-description">{{ product.description }}</p>
        <p class="product-price">價格: NT$ {{ product.price.toFixed(2) }}</p>
        <p class="product-stock">庫存: {{ product.stock }} 件</p>
        <div class="product-actions">
          <label for="quantity">數量:</label>
          <input type="number" id="quantity" v-model.number="quantity" min="1" :max="product.stock" class="quantity-input" />
          <button @click="addToCart" class="add-to-cart-button">加入購物車</button>
        </div>
      </div>
    </div>
    <div v-else-if="isLoading" class="loading-message">
      <p>載入商品資訊中...</p>
    </div>
    <div v-else class="not-found-message">
      <h1>商品未找到</h1>
      <p>抱歉，我們找不到您要查找的商品。</p>
      <router-link to="/products">返回商品列表</router-link>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import type { Product } from '@/types/product';
import { useCartStore } from '@/store/cart';
import { ElMessage } from 'element-plus';
import tidbShirtImg from '@/assets/images/tidb-shirt.png';
import htapimg from '@/assets/images/HTAP.png';
import cloudimg from '@/assets/images/cloud.png';
import pingcapimg from '@/assets/images/pingcap.png';
import tidbquiltimg from '@/assets/images/tidbquilt.png';

const route = useRoute();
const router = useRouter(); // Optional: for navigation if needed

const product = ref<Product | null>(null);
const quantity = ref<number>(1);
const isLoading = ref<boolean>(true);
const cartStore = useCartStore();

// Mock product data (same as in ProductListPage for now)
// In a real app, this would come from a shared service or store, or be fetched directly
const mockProducts: Product[] = [
  {
    id: '1',
    name: 'TiDB 官方限量版 T-Shirt',
    description: '舒適純棉，印有 TiDB Logo，開發者必備信仰充值潮服。',
    price: 25.00,
    stock: 100,
    imageUrl: tidbShirtImg,
    category: '服裝',
  },
  {
    id: '2',
    name: '高效能HTAP資料庫實戰手冊',
    description: '深入淺出 TiDB 架構與應用，從入門到精通，解鎖數據潛能。',
    price: 49.99,
    stock: 50,
    imageUrl: htapimg,
    category: '書籍',
  },
  {
    id: '3',
    name: 'TiDB 雲服務體驗券 (1個月)',
    description: '免費體驗 TiDB Cloud Developer Tier 一個月，輕鬆部署與管理您的 TiDB 叢集。',
    price: 0.00,
    stock: 200,
    imageUrl: cloudimg,
    category: '服務',
  },
  {
    id: '4',
    name: 'PingCAP 定製鍵帽組',
    description: '機械鍵盤愛好者福音，PingCAP 特色設計，為您的鍵盤增添個性。',
    price: 15.00,
    stock: 600,
    imageUrl: pingcapimg,
    category: '配件',
  },
  {
    id: '5',
    name: 'TiDB牌純棉被',
    description: '讓你蓋上之後，連作夢都在想TiDB該如何使用。',
    price: 400.00,
    stock: 50,
    imageUrl: tidbquiltimg,
    category: '家具',
  }
];

const fetchProductDetails = async () => {
  isLoading.value = true;
  const productId = route.params.id as string;

  try {
    const response = await fetch(`/api/products/${productId}`);//後端的路徑
    if (!response.ok) throw new Error('Fetch failed');

    const data = await response.json();

    // 如果庫存小於 500，加 10 元，不改變原始資料
    const adjustedProduct = {
      ...data,
      price: data.stock < 500 ? data.price + 10 : data.price,
    };

    product.value = adjustedProduct;
  } catch (error) {
    console.error('Failed to fetch product:', error);
    product.value = null;
  } finally {
    isLoading.value = false;
  }
};

const addToCart = () => {
  if (!product.value) return;

  if (quantity.value < 1) {
    ElMessage.warning('商品數量至少為 1');
    quantity.value = 1;
    return;
  }
  if (quantity.value > product.value.stock) {
    ElMessage.warning('選擇的商品數量超過庫存');
    quantity.value = product.value.stock;
    return;
  }

  cartStore.addItem(product.value, quantity.value);
  ElMessage.success(`${product.value.name} (x${quantity.value}) 已成功加入購物車！`);
};

onMounted(() => {
  fetchProductDetails();
});

// Watch for route changes if a user navigates from one product detail to another
// For example, if you have "related products" links on this page.
// import { watch } from 'vue';
// watch(() => route.params.id, (newId) => {
//   if (newId) {
//     fetchProductDetails();
//   }
// });

</script>

<style scoped>
.product-detail-page {
  max-width: 900px;
  margin: 20px auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.loading-message,
.not-found-message {
  text-align: center;
  padding: 40px;
}

.not-found-message h1 {
  color: #e74c3c;
}
.not-found-message a {
  color: #3498db;
  text-decoration: none;
}
.not-found-message a:hover {
  text-decoration: underline;
}

.product-content {
  display: flex;
  gap: 30px;
}

.product-image-container {
  flex: 1;
  max-width: 400px; /* Limit image container size */
}

.product-image {
  width: 100%;
  height: auto;
  border-radius: 8px;
  border: 1px solid #eee;
}

.product-info {
  flex: 1.5;
  display: flex;
  flex-direction: column;
}

.product-info h1 {
  font-size: 2em;
  margin-bottom: 10px;
  color: #333;
}

.product-description {
  font-size: 1em;
  color: #555;
  line-height: 1.6;
  margin-bottom: 20px;
}

.product-price {
  font-size: 1.5em;
  color: #e67e22;
  margin-bottom: 10px;
  font-weight: bold;
}

.product-stock {
  font-size: 0.9em;
  color: #7f8c8d;
  margin-bottom: 20px;
}

.product-actions {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-top: auto; /* Pushes actions to the bottom if info is short */
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.quantity-input {
  width: 70px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: center;
  font-size: 1em;
}

.add-to-cart-button {
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1em;
  transition: background-color 0.3s ease;
}

.add-to-cart-button:hover {
  background-color: #2980b9;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .product-content {
    flex-direction: column;
  }
  .product-image-container {
    max-width: 100%; /* Allow image to take full width on small screens */
    margin-bottom: 20px;
  }
  .product-info h1 {
    font-size: 1.8em;
  }
  .product-actions {
    flex-direction: column;
    align-items: stretch;
  }
  .quantity-input,
  .add-to-cart-button {
    width: 100%;
  }
}
</style> 