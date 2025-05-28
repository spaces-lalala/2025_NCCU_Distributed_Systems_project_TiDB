<template>
  <el-container direction="vertical" class="home-page">
    <!-- Section 1: Hero Section / Carousel -->
    <el-row class="hero-section" justify="center" align="middle">
      <el-col :span="24">
        <!-- Placeholder for Carousel or a prominent Hero Image/Text -->
        <div class="hero-content">
          <h2>探索最新商品</h2>
          <p>發現為您精心挑選的優質產品</p>
          <router-link to="/products">
          <el-button type="primary" size="large">立即選購</el-button>
          </router-link>
        </div>
      </el-col>
    </el-row>

    <!-- Section 2: Featured Products -->
    <el-row class="featured-products-section" justify="center">
      <el-col :span="22">
        <h3 class="section-title">熱門推薦</h3>
        <el-row :gutter="20">
          <!-- Loop for 3 Product Cards -->
          <el-col :xs="24" :sm="12" :md="8" v-for="product in mockProducts.slice(0, 3)" :key="product.id" style="margin-bottom: 20px;">
            <!-- Placeholder for ProductCard component -->
            <el-card shadow="hover">
              <img :src="product.imageUrl" class="product-image" :alt="product.name" />
              <h4>{{ product.name }}</h4>
              <p>{{ product.description }}</p>
              <div class="product-price">NT$ {{ product.price.toFixed(2) }}</div>
              <router-link :to="`/product/${product.id}`">
              <el-button type="primary" plain>查看詳情</el-button>
              </router-link>
            </el-card>
          </el-col>
        </el-row>
      </el-col>
    </el-row>

    <!-- Section 3: Bestseller Teaser -->
    <el-row class="bestseller-teaser-section" justify="center" align="middle">
      <el-col :span="18" style="text-align: center;">
        <h3 class="section-title">熱銷排行榜</h3>
        <p>看看大家都在買什麼！</p>
        <el-button type="success" size="large" @click="goToBestSellers">
          查看完整榜單
        </el-button>
      </el-col>
    </el-row>

  </el-container>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import tidbShirtImg from '@/assets/images/tidb-shirt.png';
import htapimg from '@/assets/images/HTAP.png';
import cloudimg from '@/assets/images/cloud.png';
import pingcapimg from '@/assets/images/pingcap.png';
import tidbquiltimg from '@/assets/images/tidbquilt.png';

const router = useRouter();

const mockProducts: Product[] = [
    { id: '1', name: 'TiDB 官方限量版 T-Shirt', description: '舒適純棉，印有 TiDB Logo，開發者必備信仰充值潮服。', price: 25.00, stock: 100, imageUrl: tidbShirtImg, category: '服裝' },
    { id: '2', name: '高效能HTAP資料庫實戰手冊', description: '深入淺出 TiDB 架構與應用，從入門到精通，解鎖數據潛能。', price: 49.99, stock: 50, imageUrl: htapimg, category: '書籍' },
    { id: '3', name: 'TiDB 雲服務體驗券 (1個月)', description: '免費體驗 TiDB Cloud Developer Tier 一個月，輕鬆部署與管理您的 TiDB 叢集。', price: 0.00, stock: 200, imageUrl: cloudimg, category: '服務' },
    { id: '4', name: 'PingCAP 定製鍵帽組', description: '機械鍵盤愛好者福音，PingCAP 特色設計，為您的鍵盤增添個性。', price: 15.00, stock: 75, imageUrl: pingcapimg, category: '配件' },
    { id: '5', name: 'TiDB牌純棉被', description: '讓你蓋上之後，連作夢都在想TiDB該如何使用。', price: 400.00, stock: 50, imageUrl: tidbquiltimg, category: '家具' },
  ];

// Dummy data for products, replace with API call later
// interface Product {
//   id: number;
//   name: string;
//   description: string;
//   price: number;
//   imageUrl: string;
// }
// const featuredProducts = ref<Product[]>([]);

// onMounted(async () => {
//   // TODO: Fetch featured products from API
//   // For now, using placeholders
//   try {
//    const res = await fetch('/api/products'); // 假設這是你的後端 API 路由
//    const stockData: { id: string; stock: number }[] = await res.json();

//    // 將 stock merge 到 mockProducts，並調整價格
//    const merged = mockProducts.map((mock) => {
//      const stockInfo = stockData.find(item => item.id === mock.id);
//      const updatedStock = stockInfo ? stockInfo.stock : mock.stock;
//      const adjustedPrice = updatedStock < 500 ? mock.price + 10 : mock.price;

//      return {
//        ...mock,
//        stock: updatedStock,
//        price: adjustedPrice
//      };
//    });

//    featuredProducts.value = merged.slice(0, 3);
//  } catch (error) {
//    console.error('取得庫存資料失敗', error);
//    // fallback：使用 mockProducts 原本資料
//    featuredProducts.value = mockProducts.slice(0, 3);
//  }    
// });

const goToBestSellers = () => {
  router.push('/bestsellers'); // Assuming you have a route named 'bestsellers'
};
</script>

<style scoped>
.home-page {
  /* Add overall padding or constraints if needed */
}

.hero-section {
  background-color: #f4f6f8; /* Light, neutral background */
  padding: 60px 20px;
  text-align: center;
  margin-bottom: 40px;
}

.hero-content h2 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 15px;
}

.hero-content p {
  font-size: 1.2rem;
  color: #666;
  margin-bottom: 30px;
}

.featured-products-section {
  padding: 0 20px; /* Horizontal padding for the section */
  margin-bottom: 40px;
}

.section-title {
  text-align: center;
  font-size: 1.8rem;
  color: #444;
  margin-bottom: 30px;
  font-weight: 600;
}

.el-card {
  border: 1px solid #e0e0e0; /* Softer border */
  border-radius: 8px; /* Slightly more rounded corners */
}

.product-image {
  width: 100%;
  height: 200px; /* Or use aspect-ratio */
  object-fit: cover;
  border-bottom: 1px solid #eee;
  margin-bottom: 15px;
}

.el-card h4 {
  font-size: 1.1rem;
  font-weight: 500;
  margin-bottom: 8px;
  color: #333;
}

.el-card p {
  font-size: 0.9rem;
  color: #777;
  margin-bottom: 12px;
  min-height: 3em; /* Ensure consistent height for description */
}

.product-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #d32f2f; /* A common price color */
  margin-bottom: 15px;
}

.bestseller-teaser-section {
  background-color: #e8f5e9; /* A distinct, inviting background */
  padding: 50px 20px;
  margin-top: 20px; /* Ensure some space from the previous section */
}

/* Responsive adjustments if needed */
@media (max-width: 768px) {
  .hero-content h2 {
    font-size: 2rem;
  }
  .hero-content p {
    font-size: 1rem;
  }
  .section-title {
    font-size: 1.5rem;
  }
}
</style> 