<template>
  <div class="best-sellers-page">
    <el-container>
      <el-main>
        <div class="page-header">
          <h1>熱銷排行榜</h1>
          <p>看看大家都在買什麼！</p>
        </div>

        <div v-if="isLoading" class="loading-section">
          <el-skeleton :rows="5" animated />
        </div>

        <div v-else-if="error" class="error-section">
          <el-alert :title="error" type="error" show-icon :closable="false"></el-alert>
        </div>

        <div v-else-if="bestSellers.length > 0" class="products-grid">
          <product-card 
            v-for="product in bestSellers" 
            :key="product.id" 
            :product="product"
          />
        </div>

        <div v-else class="no-products-section">
          <el-empty description="目前暫無熱銷商品數據，敬請期待！"></el-empty>
        </div>
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ProductCard from '@/components/product/ProductCard.vue'; // Corrected path
import type { Product } from '@/types/product'; // Assuming a global product type definition
import { ElContainer, ElMain, ElAlert, ElEmpty, ElSkeleton } from 'element-plus';

// If @/types/product.ts doesn't exist or is different, define Product here or create the file
// For example:
// interface Product {
//   id: string | number;
//   name: string;
//   price: number;
//   imageUrl?: string;
//   description?: string;
//   // ... other properties ProductCard might expect
// }

const bestSellers = ref<Product[]>([]);
const isLoading = ref(false);
const error = ref<string | null>(null);

const fetchBestSellers = async () => {
  isLoading.value = true;
  error.value = null;
  try {
    const response = await axios.get('/api/products/bestsellers');
    const bestSellerMap: Record<string, Product & { totalSold: number }> = {};

    // 用來儲存價格與圖片等資訊
    for (const item of response.data) {
      const id = item.productId;

      if (!bestSellerMap[id]) {
        // 模擬從 mock 資料取得價格與圖片（這邊假設每個 item 都有 price 和 imageUrl）
        bestSellerMap[id] = {
          id,
          name: item.productName,
          price: item.price ?? 0,
          imageUrl: item.imageUrl ?? '', // 如果你沒有 imageUrl，可以自己用 Map 模擬
          description: '',
          totalSold: item.totalSold ?? 0,
        };
      } else {
        bestSellerMap[id].totalSold += item.totalSold;
      }

      // 更新描述
      bestSellerMap[id].description = `已售出 ${bestSellerMap[id].totalSold} 件`;
    }

    bestSellers.value = Object.values(bestSellerMap);
  } catch (err: any) {
    console.error('Error fetching best sellers:', err);
    if (axios.isAxiosError(err) && err.response?.data?.message) {
        error.value = `無法載入熱銷商品: ${err.response.data.message}`;
    } else {
        error.value = '無法載入熱銷商品，請稍後再試。';
    }
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchBestSellers();
});
</script>

<style scoped>
.best-sellers-page {
  padding: 20px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 2.5em;
  color: #303133;
  margin-bottom: 10px;
}

.page-header p {
  font-size: 1.2em;
  color: #606266;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  justify-content: center;
}

.loading-section,
.error-section,
.no-products-section {
  padding: 40px 20px;
  text-align: center;
  margin-top: 20px;
}

/* Add styles for ProductCard if it doesn't have its own encapsulating styles for grid display */
</style> 