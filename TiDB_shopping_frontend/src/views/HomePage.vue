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
          <el-col :xs="24" :sm="12" :md="8" v-for="n in 3" :key="n" style="margin-bottom: 20px;">
            <!-- Placeholder for ProductCard component -->
            <el-card shadow="hover">
              <img src="https://via.placeholder.com/300x200?text=Product+Image" class="product-image" alt="商品圖片">
              <h4>商品名稱 {{ n }}</h4>
              <p>精簡的商品描述，吸引注意力。</p>
              <div class="product-price">NT$ {{ 100 * n }}</div>
              <el-button type="primary" plain>查看詳情</el-button>
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

const router = useRouter();

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