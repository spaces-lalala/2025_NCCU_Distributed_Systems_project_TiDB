<template>
  <div class="best-sellers-page">
    <el-container>
      <el-main>        <div class="page-header">
          <h1>🔥 熱銷排行榜</h1>
          <div class="htap-showcase">
            <div class="htap-badge">
              <i class="el-icon-lightning"></i>
              <span>TiDB HTAP 即時分析</span>
            </div>            <p class="htap-description">
              💡 <strong>真正的 HTAP 演示：</strong>此排行榜完全不依賴預計算的 sold 欄位，
              而是直接從最新的訂單交易數據即時計算真實銷量。每當有新訂單產生，
              排行榜立即反映最新結果，展現了 TiDB 混合事務分析處理（HTAP）的強大即時分析能力。
              <br><br>
              🎯 <strong>純淨體驗：</strong>我們不顯示可能不一致的銷售數字，專注於為您提供最準確的熱銷排行。
            </p>
          </div>
          <p>看看大家都在買什麼！</p>
        </div>

        <div v-if="isLoading" class="loading-section">
          <el-skeleton :rows="5" animated />
        </div>

        <div v-else-if="error" class="error-section">
          <el-alert :title="error" type="error" show-icon :closable="false"></el-alert>
        </div>        <div v-else-if="bestSellers.length > 0" class="results-section">
          <!-- HTAP 分析結果顯示 -->
          <div v-if="htapAnalysisInfo" class="htap-result">
            <i class="el-icon-success"></i>
            <span>{{ htapAnalysisInfo }}</span>
          </div>
          
          <div class="products-grid">
            <product-card 
              v-for="(product, index) in bestSellers.slice(0, 3)" 
              :key="product.id" 
              :product="product"
            >
            <template #default>
              <div class="rank-badge">第 {{ index + 1 }} 名</div>
            </template>
          </product-card>
        </div>
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

.htap-showcase {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 20px;
  margin: 20px 0;
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.htap-badge {
  display: inline-flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.2);
  padding: 8px 16px;
  border-radius: 20px;
  font-weight: bold;
  margin-bottom: 12px;
  backdrop-filter: blur(10px);
}

.htap-badge i {
  margin-right: 8px;
  color: #ffd700;
}

.htap-description {
  font-size: 14px;
  line-height: 1.6;
  margin: 0;
  opacity: 0.95;
}

.htap-result {
  background: linear-gradient(90deg, #52c41a 0%, #389e0d 100%);
  color: white;
  padding: 12px 20px;
  border-radius: 8px;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  font-weight: 500;
  box-shadow: 0 2px 8px rgba(82, 196, 26, 0.3);
}

.htap-result i {
  margin-right: 10px;
  font-size: 16px;
}

.results-section {
  margin-top: 20px;
}

.products-grid {
  display: flex;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  justify-content: center;
  flex-wrap: nowrap;
}

.loading-section,
.error-section,
.no-products-section {
  padding: 40px 20px;
  text-align: center;
  margin-top: 20px;
}

/* Add styles for ProductCard if it doesn't have its own encapsulating styles for grid display */

.rank-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background-color: #f56c6c;
  color: white;
  font-weight: bold;
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 0.9em;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  z-index: 10;
}

</style>