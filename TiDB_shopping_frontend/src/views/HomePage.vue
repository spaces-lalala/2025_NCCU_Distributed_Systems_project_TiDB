<template>
  <div class="home-page">
    <el-carousel height="400px" class="hero-carousel">
      <el-carousel-item v-for="item in heroItems" :key="item.id">
        <img :src="item.imageUrl" :alt="item.altText" class="hero-image" />
        <div class="hero-caption">
          <h3>{{ item.title }}</h3>
          <p>{{ item.subtitle }}</p>
        </div>
      </el-carousel-item>
    </el-carousel>

    <section class="featured-products">
      <h2 class="section-title">熱門商品推薦</h2>
      <el-row :gutter="20">
        <el-col :xs="24" :sm="12" :md="8" v-for="product in featuredProducts" :key="product.id">
          <ProductCard :product="product" @view-details="goToProductDetails" />
        </el-col>
      </el-row>
    </section>

    <section class="bestsellers-teaser">
      <h2 class="section-title">熱銷排行榜</h2>
      <p>探索我們最受歡迎的商品！</p>
      <router-link to="/bestsellers">
        <el-button type="primary" size="large">前往熱銷榜</el-button>
      </router-link>
    </section>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ProductCard from '@/components/product/ProductCard.vue';
import type { Product } from '@/types/domain'; // Assuming Product type is defined
// import productService from '@/services/productService'; // Placeholder for actual service

const router = useRouter();

// --- Hero Carousel Items --- (Can be fetched from API or be static)
const heroItems = ref([
  {
    id: 1,
    imageUrl: 'https://via.placeholder.com/1200x400.png?text=Featured+Product+1',
    altText: '特色商品1',
    title: 'TiDB 官方限量版 T-Shirt',
    subtitle: '開發者必備信仰充值潮服，舒適純棉。'
  },
  {
    id: 2,
    imageUrl: 'https://via.placeholder.com/1200x400.png?text=Special+Offer',
    altText: '特別優惠',
    title: '高效能HTAP資料庫實戰手冊',
    subtitle: '深入淺出 TiDB 架構與應用，解鎖數據潛能。'
  },
  {
    id: 3,
    imageUrl: 'https://via.placeholder.com/1200x400.png?text=New+Arrivals',
    altText: '新品上市',
    title: 'TiDB 雲服務體驗券 (1個月)',
    subtitle: '免費體驗 TiDB Cloud Developer Tier。'
  }
]);

// --- Featured Products --- (Initial 3-5 products as per plan)
const featuredProducts = ref<Product[]>([]);

// Mock data for initial products, aligning with the plan
const initialMockProducts: Product[] = [
  {
    id: 'prod_001',
    name: 'TiDB 官方限量版 T-Shirt',
    description: '舒適純棉，印有 TiDB Logo，開發者必備信仰充值潮服。',
    price: 25.00,
    stock: 100,
    category: '服裝',
    image_url: 'https://via.placeholder.com/400x300.png?text=TiDB+T-Shirt', // Replace with actual or better placeholder
  },
  {
    id: 'prod_002',
    name: '高效能HTAP資料庫實戰手冊',
    description: '深入淺出 TiDB 架構與應用，從入門到精通，解鎖數據潛能。',
    price: 49.99,
    stock: 50,
    category: '書籍',
    image_url: 'https://via.placeholder.com/400x300.png?text=TiDB+Handbook',
  },
  {
    id: 'prod_003',
    name: 'TiDB 雲服務體驗券 (1個月)',
    description: '免費體驗 TiDB Cloud Developer Tier 一個月，輕鬆部署與管理您的 TiDB 叢集。',
    price: 1.00, // Plan suggests 0.00 or small amount
    stock: 200,
    category: '服務',
    image_url: 'https://via.placeholder.com/400x300.png?text=TiDB+Cloud+Voucher',
  },
];

const fetchFeaturedProducts = async () => {
  // In a real application, you would fetch this from an API:
  // try {
  //   featuredProducts.value = await productService.getProducts({ limit: 3, /* other params */ });
  // } catch (error) {
  //   console.error("Failed to fetch featured products:", error);
  //   // Fallback to mock data if API call fails
  //   featuredProducts.value = initialMockProducts.slice(0, 3);
  // }

  // For now, using mock data directly
  featuredProducts.value = initialMockProducts.slice(0, 3);
};

onMounted(() => {
  fetchFeaturedProducts();
});

const goToProductDetails = (productId: string | number) => {
  router.push({ name: 'ProductDetail', params: { id: productId } });
};

</script>

<style scoped>
.home-page {
  padding: 0; /* Remove default padding if app-main-content has it */
}

.hero-carousel {
  margin-bottom: 40px;
}

.hero-image {
  width: 100%;
  height: 400px;
  object-fit: cover;
}

.hero-caption {
  position: absolute;
  bottom: 20px;
  left: 20px;
  background-color: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 15px;
  border-radius: 5px;
}

.hero-caption h3 {
  margin-top: 0;
  font-size: 2em;
}

.hero-caption p {
  font-size: 1.2em;
  margin-bottom: 0;
}

.section-title {
  font-size: 1.8em;
  font-weight: 600;
  margin-bottom: 20px;
  text-align: center;
  color: #303133;
}

.featured-products {
  margin-bottom: 40px;
  padding: 0 20px; /* Add some horizontal padding for content */
}

.bestsellers-teaser {
  text-align: center;
  padding: 40px 20px;
  background-color: #f9f9f9; /* Light background for emphasis */
  border-top: 1px solid #e0e0e0;
  border-bottom: 1px solid #e0e0e0;
  margin-bottom: 40px;
}

.bestsellers-teaser p {
  font-size: 1.1em;
  color: #606266;
  margin-bottom: 20px;
}
</style> 