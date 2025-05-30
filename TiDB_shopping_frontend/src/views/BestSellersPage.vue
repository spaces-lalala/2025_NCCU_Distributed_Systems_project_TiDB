<template>
  <div class="best-sellers-page">
    <!-- Page Header -->
    <section class="page-header">
      <h1 class="page-title">🔥 熱銷排行榜</h1>
      
      <!-- HTAP Showcase -->
      <div class="htap-showcase">
        <div class="htap-badge">
          <i class="el-icon-lightning"></i>
          <span>TiDB HTAP 即時分析</span>
        </div>
        <div class="htap-description">
          <p>
            <strong>真正的 HTAP 演示：</strong>此排行榜完全不依賴預計算的 sold 欄位，
            而是直接從最新的訂單交易數據即時計算真實銷量。每當有新訂單產生，
            排行榜立即反映最新結果，展現了 TiDB 混合事務分析處理（HTAP）的強大即時分析能力。
          </p>
          <p>
            <strong>純淨體驗：</strong>我們不顯示可能不一致的銷售數字，專注於為您提供最準確的熱銷排行。
          </p>
        </div>
      </div>
      
      <p class="page-subtitle">看看大家都在買什麼！</p>
    </section>

    <!-- Loading State -->
    <section v-if="isLoading" class="loading-section">
      <el-skeleton :rows="5" animated />
    </section>

    <!-- Error State -->
    <section v-else-if="error" class="error-section">
      <el-alert :title="error" type="error" show-icon :closable="false" />
    </section>

    <!-- Results Section -->
    <section v-else-if="bestSellers.length > 0" class="results-section">
      <!-- HTAP Analysis Result -->
      <div v-if="htapAnalysisInfo" class="htap-result">
        <i class="el-icon-success"></i>
        <span>{{ htapAnalysisInfo }}</span>
      </div>
      
      <!-- Products Grid -->
      <div class="products-grid">
        <div 
          v-for="(product, index) in bestSellers.slice(0, 3)" 
          :key="product.id" 
          class="bestseller-card"
        >
          <div class="rank-badge">
            第 {{ index + 1 }} 名
          </div>
          <product-card :product="product" />
        </div>
      </div>
    </section>    <!-- No Products -->
    <section v-else class="no-products-section">
      <el-empty description="目前暫無熱銷商品數據，敬請期待！" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import axios from 'axios';
import ProductCard from '@/components/product/ProductCard.vue'; // Corrected path
import type { Product } from '@/types/product'; // Assuming a global product type definition
import { ElContainer, ElMain, ElAlert, ElEmpty, ElSkeleton } from 'element-plus';

import { productImageMap } from '@/assets/images/ProductImageMaps';

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
const htapAnalysisInfo = ref<string>('');

const fetchBestSellers = async () => {
  isLoading.value = true;
  error.value = null;
  htapAnalysisInfo.value = '';

  try {
    const response = await axios.get('/api/products/bestsellers');    bestSellers.value = response.data.map((item: any, index: number) => ({
      id: item.id,
      name: item.name,
      price: item.price,
      imageUrl: productImageMap[item.name] ?? item.image_url ?? '',
      description: `精選熱銷商品`, // 移除銷售數量顯示，避免混淆
    }));    // 設置 HTAP 分析提示 - 不依賴可能不準確的 sold 欄位
    htapAnalysisInfo.value = `✨ TiDB HTAP 即時分析：基於最新交易數據計算熱銷排行，排序完全來自真實訂單記錄`;
    
  } catch (err: any) {
    console.error('Error fetching best sellers:', err);
    error.value = '無法載入熱銷商品，請稍後再試。';
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
  margin-bottom: var(--spacing-lg);
}

.page-subtitle {
  font-size: var(--font-size-lg);
  color: var(--text-secondary);
  margin-bottom: 0;
}

/* HTAP Showcase */
.htap-showcase {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  border-radius: var(--border-radius-large);
  padding: var(--spacing-xl);
  margin: var(--spacing-lg) 0;
  color: white;
  box-shadow: var(--shadow-dark);
}

.htap-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.2);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: 20px;
  font-weight: 600;
  margin-bottom: var(--spacing-md);
  backdrop-filter: blur(10px);
  font-size: var(--font-size-sm);
}

.htap-badge i {
  margin-right: var(--spacing-xs);
  color: #ffd700;
}

.htap-description {
  font-size: var(--font-size-sm);
  line-height: 1.6;
  opacity: 0.95;
}

.htap-description p {
  margin-bottom: var(--spacing-md);
}

.htap-description p:last-child {
  margin-bottom: 0;
}

/* HTAP Result */
.htap-result {
  background: linear-gradient(90deg, var(--success-color) 0%, #52c41a 100%);
  color: white;
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-base);
  margin-bottom: var(--spacing-lg);
  display: flex;
  align-items: center;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(82, 196, 26, 0.3);
}

.htap-result i {
  margin-right: var(--spacing-sm);
  font-size: var(--font-size-base);
}

/* Products Grid */
.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-lg);
  justify-items: center;
}

.bestseller-card {
  position: relative;
  width: 100%;
  max-width: 320px;
}

.rank-badge {
  position: absolute;
  top: var(--spacing-sm);
  left: var(--spacing-sm);
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-base);
  font-size: var(--font-size-xs);
  font-weight: 700;
  z-index: 10;
  box-shadow: var(--shadow-base);
}

/* States */
.loading-section,
.error-section,
.no-products-section {
  background-color: var(--bg-color);
  border-radius: var(--border-radius-base);
  padding: var(--spacing-xxl);
  text-align: center;
  box-shadow: var(--shadow-light);
}

/* 響應式設計 */
@media (max-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .page-title {
    font-size: var(--font-size-xxl);
  }
  
  .htap-showcase {
    padding: var(--spacing-lg);
    margin-left: calc(-1 * var(--spacing-lg));
    margin-right: calc(-1 * var(--spacing-lg));
    border-radius: 0;
  }
  
  .products-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
    .bestseller-card {
    max-width: 100%;
  }
}
</style>