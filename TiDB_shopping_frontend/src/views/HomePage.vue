<template>
  <div class="home-page">
    <!-- Hero Section -->
    <section class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">探索最新商品</h1>
        <p class="hero-description">發現為您精心挑選的優質產品</p>
        <router-link to="/products">
          <el-button type="primary" size="large" class="cta-button">
            立即選購
          </el-button>
        </router-link>
      </div>
    </section>

    <!-- Featured Products Section -->
    <section class="featured-section">
      <div class="section-header">
        <h2 class="section-title">熱門推薦</h2>
        <p class="section-description">精選高品質商品</p>
      </div>
      
      <div class="products-grid grid-3">
        <div 
          v-for="product in featuredProducts.slice(0, 3)" 
          :key="product.id" 
          class="product-card"
        >
          <div class="product-image-container">
            <img 
              :src="product.imageUrl" 
              class="product-image" 
              :alt="product.name"
            />
          </div>
          <div class="product-info">
            <h4 class="product-name">{{ product.name }}</h4>
            <p class="product-description">{{ product.description }}</p>
            <div class="product-price">NT$ {{ (product.price || 0).toFixed(2) }}</div>
            <router-link :to="`/product/${product.id}`">
              <el-button type="primary" plain class="product-button">
                查看詳情
              </el-button>
            </router-link>
          </div>
        </div>
      </div>
    </section>

    <!-- Bestseller Teaser Section -->
    <section class="bestseller-section">
      <div class="bestseller-content">
        <h2 class="section-title">熱銷排行榜</h2>
        <p class="section-description">看看大家都在買什麼！</p>
        <el-button 
          type="success" 
          size="large" 
          @click="goToBestSellers"
          class="cta-button"
        >
          查看完整榜單
        </el-button>
      </div>
    </section>
  </div>
</template>

<script lang="ts" setup>
import { useRouter } from 'vue-router';
import { ref, onMounted } from 'vue';
import { productImageMap } from '@/assets/images/ProductImageMaps';
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
interface Product {
  id: string;
  name: string;
  description: string;
  price: number;
  stock: number;
  imageUrl: string;
  category: string;
}
 const featuredProducts = ref<Product[]>([]);

onMounted(async () => {
  try {
    const response = await fetch("http://localhost:8000/api/products");
    const allProducts: Product[] = await response.json();

    // 對每個產品應用圖片轉換邏輯
    featuredProducts.value = allProducts.slice(0, 3).map(product => {
      const stock = Number(product.stock);
      const price = Number(product.price);
      return {
        ...product,
        imageUrl: productImageMap[product.name] ?? product.image_url ?? '',
        price: stock < 500 ? price + 10 : price,
        stock,
      };
    });
  } catch (error) {
    console.error('取得商品資料失敗', error);
  }
});

const goToBestSellers = () => {
  router.push('/bestsellers'); // Assuming you have a route named 'bestsellers'
};
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xxl);
}

/* Hero Section */
.hero-section {
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-dark) 100%);
  color: white;
  padding: var(--spacing-xxl) var(--spacing-lg);
  border-radius: var(--border-radius-large);
  text-align: center;
  margin-bottom: var(--spacing-lg);
}

.hero-content {
  max-width: 600px;
  margin: 0 auto;
}

.hero-title {
  font-size: var(--font-size-xxxl);
  font-weight: 700;
  margin-bottom: var(--spacing-md);
  color: white;
}

.hero-description {
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-xl);
  opacity: 0.9;
  color: white;
}

.cta-button {
  padding: var(--spacing-md) var(--spacing-xl);
  font-size: var(--font-size-base);
  font-weight: 600;
}

/* Featured Section */
.featured-section {
  background-color: var(--bg-color);
  padding: var(--spacing-xxl);
  border-radius: var(--border-radius-large);
  box-shadow: var(--shadow-light);
}

.section-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.section-title {
  font-size: var(--font-size-xxl);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.section-description {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  margin-bottom: 0;
}

/* Product Cards */
.products-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-lg);
}

.product-card {
  background-color: var(--bg-color);
  border: 1px solid var(--border-lighter);
  border-radius: var(--border-radius-base);
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-light);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-dark);
}

.product-image-container {
  position: relative;
  width: 100%;
  height: 240px;
  overflow: hidden;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.product-info {
  padding: var(--spacing-lg);
}

.product-name {
  font-size: var(--font-size-lg);
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
  line-height: 1.4;
}

.product-description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin-bottom: var(--spacing-md);
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-price {
  font-size: var(--font-size-xl);
  font-weight: 700;
  color: var(--danger-color);
  margin-bottom: var(--spacing-md);
}

.product-button {
  width: 100%;
  font-weight: 500;
}

/* Bestseller Section */
.bestseller-section {
  background: linear-gradient(135deg, var(--success-color) 0%, #52c41a 100%);
  color: white;
  padding: var(--spacing-xxl);
  border-radius: var(--border-radius-large);
  text-align: center;
}

.bestseller-content .section-title,
.bestseller-content .section-description {
  color: white;
}

.bestseller-content .section-description {
  opacity: 0.9;
}

/* 響應式設計 */
@media (max-width: 1024px) {
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .home-page {
    gap: var(--spacing-lg);
  }
  
  .hero-section,
  .featured-section,
  .bestseller-section {
    padding: var(--spacing-lg);
    margin-left: calc(-1 * var(--spacing-lg));
    margin-right: calc(-1 * var(--spacing-lg));
    border-radius: 0;
  }
  
  .hero-title {
    font-size: var(--font-size-xxl);
  }
  
  .hero-description {
    font-size: var(--font-size-base);
  }
  
  .products-grid {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .product-image-container {
    height: 200px;
  }
}
</style>