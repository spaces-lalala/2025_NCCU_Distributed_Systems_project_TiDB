<template>
  <div class="product-list-page">
    <h1 class="page-title">所有商品</h1>

    <!-- Future: Filters and Sorting section -->
    <!-- 
    <el-row :gutter="20" class="controls-section">
      <el-col :span="18">
        Filters: (Category, Price Range, etc.)
      </el-col>
      <el-col :span="6">
        Sort by: (Price, Popularity, etc.)
      </el-col>
    </el-row>
    -->

    <el-row v-if="isLoading" class="loading-indicator">
      <el-col :span="24">
        <el-skeleton :rows="10" animated />
      </el-col>
    </el-row>
    
    <el-empty v-if="!isLoading && paginatedProducts.length === 0" description="暫無商品"></el-empty>

    <el-row v-if="!isLoading && paginatedProducts.length > 0" :gutter="20">
      <el-col :xs="24" :sm="12" :md="8" :lg="6" v-for="product in paginatedProducts" :key="product.id">
        <ProductCard :product="product" @view-details="goToProductDetails" />
      </el-col>
    </el-row>

    <el-row v-if="!isLoading && totalProducts > pageSize" justify="center" class="pagination-container">
      <el-pagination
        background
        layout="prev, pager, next, jumper, ->, total"
        :total="totalProducts"
        :page-size="pageSize"
        :current-page="currentPage"
        @current-change="handlePageChange"
      />
    </el-row>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ProductCard from '@/components/product/ProductCard.vue';
import type { Product } from '@/types/domain';
// import productService from '@/services/productService'; // Placeholder

const router = useRouter();

const allProducts = ref<Product[]>([]);
const isLoading = ref<boolean>(true);
const currentPage = ref<number>(1);
const pageSize = ref<number>(12); // Number of products per page

// Extended mock data for product list page
const mockProductData: Product[] = Array.from({ length: 35 }, (_, i) => ({
  id: `prod_list_${i + 1}`,
  name: `精選商品 ${i + 1} - 高品質選擇`,
  description: `這是精選商品 ${i + 1} 的詳細描述，提供無與倫比的價值和體驗。採用最新技術和最優質材料製成。`,
  price: parseFloat((Math.random() * 100 + 10).toFixed(2)), // Random price between 10 and 110
  stock: Math.floor(Math.random() * 200 + 1),
  category: i % 3 === 0 ? '電子產品' : i % 3 === 1 ? '生活家居' : '時尚服飾',
  image_url: `https://via.placeholder.com/400x300.png?text=商品+${i + 1}`,
}));

const totalProducts = computed(() => allProducts.value.length);

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  return allProducts.value.slice(start, end);
});

const fetchAllProducts = async () => {
  isLoading.value = true;
  // Simulate API call delay
  await new Promise(resolve => setTimeout(resolve, 1000)); 
  // In a real application, use the productService:
  // try {
  //   allProducts.value = await productService.getAllProducts({ page: currentPage.value, limit: pageSize.value, /* other params */ });
  //   // If API handles pagination, totalProducts might come from API response metadata
  // } catch (error) {
  //   console.error("Failed to fetch all products:", error);
  //   allProducts.value = mockProductData; // Fallback or show error
  // }

  // For now, using mock data directly for all products
  allProducts.value = mockProductData;
  isLoading.value = false;
};

onMounted(() => {
  fetchAllProducts();
});

const handlePageChange = (newPage: number) => {
  currentPage.value = newPage;
  // If API handles pagination, you might refetch products for the new page here
  // fetchAllProducts(); 
  // For client-side pagination, scrolling to top might be good UX
  window.scrollTo({ top: 0, behavior: 'smooth' });
};

const goToProductDetails = (productId: string | number) => {
  router.push({ name: 'ProductDetail', params: { id: productId } });
};
</script>

<style scoped>
.product-list-page {
  padding: 20px;
}

.page-title {
  text-align: center;
  font-size: 2em;
  margin-bottom: 30px;
  color: #303133;
}

.controls-section {
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.loading-indicator {
  margin-top: 40px;
}

.pagination-container {
  margin-top: 30px;
  padding-bottom: 20px; /* Ensure space below pagination */
}

/* Ensure product cards are spaced nicely */
.el-col {
  margin-bottom: 20px; /* Add bottom margin to columns for spacing between rows */
}
</style> 