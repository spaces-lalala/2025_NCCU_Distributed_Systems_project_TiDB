<template>
  <div class="product-detail-page">
    <el-breadcrumb separator="/" class="breadcrumb-nav">
      <el-breadcrumb-item :to="{ path: '/' }">首頁</el-breadcrumb-item>
      <el-breadcrumb-item :to="{ path: '/products' }">商品列表</el-breadcrumb-item>
      <el-breadcrumb-item v-if="product">{{ product.name }}</el-breadcrumb-item>
      <el-breadcrumb-item v-else>商品詳情</el-breadcrumb-item>
    </el-breadcrumb>

    <el-skeleton :rows="10" animated v-if="isLoading" />

    <el-empty description="找不到該商品" v-if="!isLoading && !product">
      <el-button type="primary" @click="router.push('/products')">返回商品列表</el-button>
    </el-empty>

    <el-row :gutter="30" v-if="!isLoading && product" class="product-content">
      <el-col :xs="24" :md="10" class="product-gallery">
        <!-- Main Image -->
        <img :src="selectedImage || product.image_url || defaultImage" class="main-product-image" @error="onMainImageError" />
        <!-- Thumbnail Images (optional) -->
        <el-row :gutter="10" class="thumbnail-strip" v-if="product.images && product.images.length > 1">
          <el-col :span="6" v-for="(imgUrl, index) in product.images" :key="index">
            <img 
              :src="imgUrl || defaultImage" 
              class="thumbnail-image" 
              :class="{ active: selectedImage === imgUrl }"
              @click="selectedImage = imgUrl"
              @error="onThumbnailError"
            />
          </el-col>
        </el-row>
      </el-col>

      <el-col :xs="24" :md="14" class="product-info">
        <h1 class="product-title">{{ product.name }}</h1>
        <p class="product-category">分類: {{ product.category || '未分類' }}</p>
        
        <el-descriptions :column="1" border class="product-specs">
          <el-descriptions-item label="價格">
            <span class="price">￥{{ product.price.toFixed(2) }}</span>
          </el-descriptions-item>
          <el-descriptions-item label="庫存">
            <el-tag :type="product.stock > 0 ? 'success' : 'danger'">
              {{ product.stock > 0 ? `尚有 ${product.stock} 件` : '已售罄' }}
            </el-tag>
          </el-descriptions-item>
          <el-descriptions-item label="描述">
            {{ product.description }}
          </el-descriptions-item>
          <!-- Add more specifications if available -->
        </el-descriptions>
        
        <div class="quantity-control" v-if="product.stock > 0">
          <span class="quantity-label">數量:</span>
          <el-input-number v-model="quantity" :min="1" :max="product.stock" />
        </div>
        
        <div class="action-buttons">
          <el-button 
            type="warning" 
            size="large" 
            @click="handleAddToCart" 
            :disabled="product.stock === 0"
            :icon="ShoppingCart"
          >
            加入購物車
          </el-button>
          <el-button type="danger" plain size="large" @click="buyNow" :disabled="product.stock === 0">
            立即購買
          </el-button>
        </div>
      </el-col>
    </el-row>

    <!-- Related Products Section (Optional) -->
    <!-- 
    <section class="related-products" v-if="!isLoading && product">
      <h2 class="section-title">相關推薦</h2>
      <p>...</p>
    </section>
    -->
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ElMessage, ElMessageBox } from 'element-plus';
import { ShoppingCart } from '@element-plus/icons-vue';
import { useCartStore } from '@/store/cart';
import type { Product } from '@/types/domain';
// import productService from '@/services/productService'; // Placeholder

const route = useRoute();
const router = useRouter();
const cartStore = useCartStore();

const product = ref<Product | null>(null);
const isLoading = ref<boolean>(true);
const quantity = ref<number>(1);
const selectedImage = ref<string | undefined>(undefined);

const defaultImage = 'https://via.placeholder.com/600x400.png?text=No+Image';

// Extended mock data, including the ones from HomePage and ProductListPage for consistency
const allMockProducts: Product[] = [
  // From HomePage
  {
    id: 'prod_001',
    name: 'TiDB 官方限量版 T-Shirt',
    description: '舒適純棉，印有 TiDB Logo，開發者必備信仰充值潮服。採用高品質棉料，透氣舒適，多種尺寸可選。',
    price: 25.00,
    stock: 100,
    category: '服裝',
    image_url: 'https://via.placeholder.com/600x400.png?text=TiDB+T-Shirt',
    images: [
      'https://via.placeholder.com/600x400.png?text=T-Shirt+View+1',
      'https://via.placeholder.com/600x400.png?text=T-Shirt+View+2',
      'https://via.placeholder.com/600x400.png?text=T-Shirt+Detail',
    ]
  },
  {
    id: 'prod_002',
    name: '高效能HTAP資料庫實戰手冊',
    description: '深入淺出 TiDB 架構與應用，從入門到精通，解鎖數據潛能。包含大量實戰案例和最佳實踐。',
    price: 49.99,
    stock: 50,
    category: '書籍',
    image_url: 'https://via.placeholder.com/600x400.png?text=TiDB+Handbook',
  },
  {
    id: 'prod_003',
    name: 'TiDB 雲服務體驗券 (1個月)',
    description: '免費體驗 TiDB Cloud Developer Tier 一個月，輕鬆部署與管理您的 TiDB 叢集。探索無限可能。',
    price: 1.00,
    stock: 0, // Intentionally out of stock for demo
    category: '服務',
    image_url: 'https://via.placeholder.com/600x400.png?text=TiDB+Cloud+Voucher',
  },
  // From ProductListPage (ensuring IDs are unique or handled)
  ...Array.from({ length: 35 }, (_, i) => ({
    id: `prod_list_${i + 1}`,
    name: `精選商品 ${i + 1} - 高品質選擇`,
    description: `這是精選商品 ${i + 1} 的詳細描述，提供無與倫比的價值和體驗。採用最新技術和最優質材料製成。適合各種場合，是您的理想之選。`,
    price: parseFloat((Math.random() * 100 + 10).toFixed(2)),
    stock: Math.floor(Math.random() * 200 + 1),
    category: i % 3 === 0 ? '電子產品' : i % 3 === 1 ? '生活家居' : '時尚服飾',
    image_url: `https://via.placeholder.com/600x400.png?text=商品+${i + 1}`,
    images: [
      `https://via.placeholder.com/600x400.png?text=商品+${i + 1}+View+1`,
      `https://via.placeholder.com/600x400.png?text=商品+${i + 1}+View+2`,
    ]
  }))
];

const productId = computed(() => route.params.id as string);

const fetchProductDetails = async (id: string) => {
  isLoading.value = true;
  product.value = null;
  selectedImage.value = undefined;
  quantity.value = 1;

  await new Promise(resolve => setTimeout(resolve, 700)); // Simulate API delay
  // In a real application:
  // try {
  //   product.value = await productService.getProductById(id);
  //   if (product.value && product.value.images && product.value.images.length > 0) {
  //     selectedImage.value = product.value.images[0];
  //   }
  // } catch (error) {
  //   console.error(`Failed to fetch product ${id}:`, error);
  //   product.value = null;
  // }

  // For now, using mock data
  const foundProduct = allMockProducts.find(p => p.id === id);
  product.value = foundProduct || null;
  if (product.value && product.value.images && product.value.images.length > 0) {
    selectedImage.value = product.value.images[0];
  } else if (product.value) {
    selectedImage.value = product.value.image_url;
  }
  isLoading.value = false;
};

const handleAddToCart = () => {
  if (product.value && product.value.stock > 0 && quantity.value > 0) {
    cartStore.addItem(product.value, quantity.value);
    ElMessage.success(`${product.value.name} (x${quantity.value}) 已加入購物車`);
  } else {
    ElMessage.warning('商品庫存不足或數量無效');
  }
};

const buyNow = () => {
  if (product.value && product.value.stock > 0 && quantity.value > 0) {
    // For "Buy Now", typically add to cart and redirect to checkout immediately
    cartStore.addItem(product.value, quantity.value); // Add to cart first
    router.push('/checkout');
  } else {
     ElMessage.warning('商品庫存不足或數量無效');
  }
};

const onMainImageError = (event: Event) => {
  const imgElement = event.target as HTMLImageElement;
  imgElement.src = defaultImage;
};
const onThumbnailError = (event: Event) => {
  const imgElement = event.target as HTMLImageElement;
  imgElement.src = 'https://via.placeholder.com/100x75.png?text=Error'; // Smaller error placeholder for thumbnails
};

// Fetch product details when component is mounted and when productId changes
onMounted(() => {
  if (productId.value) {
    fetchProductDetails(productId.value);
  }
});

watch(productId, (newId, oldId) => {
  if (newId && newId !== oldId) {
    fetchProductDetails(newId);
  }
});

</script>

<style scoped>
.product-detail-page {
  padding: 20px;
}

.breadcrumb-nav {
  margin-bottom: 25px;
  font-size: 1em;
}

.product-content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0,0,0,0.1);
}

.product-gallery {
  text-align: center;
}

.main-product-image {
  max-width: 100%;
  max-height: 450px;
  object-fit: contain;
  border-radius: 4px;
  margin-bottom: 15px;
  border: 1px solid #ebeef5;
}

.thumbnail-strip {
  margin-top: 10px;
}

.thumbnail-image {
  width: 100%;
  height: 75px;
  object-fit: cover;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.2s, border-color 0.2s;
}

.thumbnail-image:hover,
.thumbnail-image.active {
  opacity: 1;
  border-color: var(--el-color-primary);
}

.product-info {
  /* Styles for product information column */
}

.product-title {
  font-size: 2em;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 10px;
  color: #303133;
}

.product-category {
  font-size: 0.9em;
  color: #909399;
  margin-bottom: 20px;
}

.product-specs {
  margin-bottom: 25px;
}

.product-specs .price {
  font-size: 1.8em;
  font-weight: bold;
  color: var(--el-color-danger);
}

.quantity-control {
  margin-bottom: 25px;
  display: flex;
  align-items: center;
}

.quantity-label {
  margin-right: 10px;
  font-size: 1em;
  color: #606266;
}

.action-buttons .el-button {
  margin-right: 15px;
  min-width: 150px; /* Ensure buttons have a decent width */
}

.section-title {
  font-size: 1.6em;
  font-weight: 600;
  margin-top: 40px;
  margin-bottom: 20px;
  text-align: center;
  color: #303133;
  border-bottom: 1px solid #ebeef5;
  padding-bottom: 10px;
}
</style> 