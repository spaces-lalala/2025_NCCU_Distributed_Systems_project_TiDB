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
    if (!response.ok) throw new Error('Fetch failed');

    const data: Product = await response.json();
    // 調整價格：庫存小於 500 就漲價 10 元
    const adjustedPrice = data.stock < 500 ? data.price + 10 : data.price;

    // 若有需要調整圖片欄位
    product.value = {
      ...data,
      price: adjustedPrice, // 覆蓋價格
      // imageUrl: data.image_url,  // 轉換圖片欄位
      imageUrl: productImageMap[data.name] ?? data.image_url ?? '', // 優先用 map，再 fallback
    };
  } catch (error) {
    console.error('商品讀取失敗：', error);
    product.value = null;
  } finally {
    isLoading.value = false;
  }
};


const addToCart = async () => {
  if (!product.value) return;

  if (quantity.value < 1) {
    ElMessage.warning('商品數量至少為 1');
    quantity.value = 1;
    return;
  }

  // 實時檢查庫存
  try {
    const response = await fetch(`/api/products/${product.value.id}`);
    if (!response.ok) throw new Error('庫存檢查失敗');
    
    const currentStock = await response.json();
    const availableStock = currentStock.stock;

    if (availableStock <= 0) {
      ElMessage.error('商品已售完，無法加入購物車');
      product.value.stock = 0; // 更新本地庫存顯示
      return;
    }

    if (quantity.value > availableStock) {
      ElMessage.warning(`庫存不足，目前僅剩 ${availableStock} 件`);
      quantity.value = availableStock;
      product.value.stock = availableStock; // 更新本地庫存顯示
      return;
    }

    // 檢查購物車中已有的數量
    const cartItem = cartStore.getCartItems.find(item => item.id === product.value!.id);
    const cartQuantity = cartItem ? cartItem.quantity : 0;
    
    if (cartQuantity + quantity.value > availableStock) {
      const maxAddable = availableStock - cartQuantity;
      if (maxAddable <= 0) {
        ElMessage.warning('您購物車中此商品的數量已達到庫存上限');
        return;
      }
      ElMessage.warning(`加上購物車中的數量將超過庫存，最多還可加入 ${maxAddable} 件`);
      quantity.value = maxAddable;
      return;
    }

    // 更新本地商品庫存資訊
    product.value.stock = availableStock;
    
    cartStore.addItem(product.value, quantity.value);
    ElMessage.success(`${product.value.name} (x${quantity.value}) 已成功加入購物車！`);
  } catch (error) {
    console.error('庫存驗證失敗：', error);
    ElMessage.error('無法驗證庫存，請稍後再試');
  }
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