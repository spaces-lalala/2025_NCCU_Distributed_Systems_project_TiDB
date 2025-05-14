<template>
  <div class="product-list-page">
    <h1>商品列表</h1>
    <div v-if="products.length > 0" class="product-grid">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </div>
    <div v-else class="no-products">
      <p>目前沒有商品可供展示。</p>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import ProductCard from '@/components/product/ProductCard.vue';
import type { Product } from '@/types/product'; // Assuming you have a type definition for Product

// Define a reactive variable to hold the products
const products = ref<Product[]>([]);

// Mock data based on the plan (section 4.1)
// You should replace this with an API call in a real application
const fetchProducts = async () => {
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 500));
  
  products.value = [
    {
      id: '1',
      name: 'TiDB 官方限量版 T-Shirt',
      description: '舒適純棉，印有 TiDB Logo，開發者必備信仰充值潮服。',
      price: 25.00,
      stock: 100,
      image_url: 'https://via.placeholder.com/300x200.png?text=TiDB+T-Shirt', // Placeholder image
      category: '服裝',
    },
    {
      id: '2',
      name: '高效能HTAP資料庫實戰手冊',
      description: '深入淺出 TiDB 架構與應用，從入門到精通，解鎖數據潛能。',
      price: 49.99,
      stock: 50,
      image_url: 'https://via.placeholder.com/300x200.png?text=TiDB+Handbook', // Placeholder image
      category: '書籍',
    },
    {
      id: '3',
      name: 'TiDB 雲服務體驗券 (1個月)',
      description: '免費體驗 TiDB Cloud Developer Tier 一個月，輕鬆部署與管理您的 TiDB 叢集。',
      price: 0.00,
      stock: 200,
      image_url: 'https://via.placeholder.com/300x200.png?text=TiDB+Cloud+Voucher', // Placeholder image
      category: '服務',
    },
    {
      id: '4',
      name: 'PingCAP 定製鍵帽組',
      description: '機械鍵盤愛好者福音，PingCAP 特色設計，為您的鍵盤增添個性。',
      price: 15.00,
      stock: 75,
      image_url: 'https://via.placeholder.com/300x200.png?text=PingCAP+Keycaps', // Placeholder image
      category: '配件',
    }
  ];
};

onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
.product-list-page {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
}

h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.no-products {
  text-align: center;
  margin-top: 50px;
}

.no-products p {
  font-size: 1.2em;
  color: #777;
}
</style> 