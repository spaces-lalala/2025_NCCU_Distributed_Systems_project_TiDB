<template>
  <el-container class="product-list-page" ref="pageContainerRef">
    <!-- Sidebar for Filters (Visible on larger screens) -->
    <el-aside width="260px" class="filter-sidebar" v-if="!isSmallScreen">
      <h3>篩選條件</h3>
      <el-divider />
      <div class="filter-group">
        <h4>分類</h4>
        <el-checkbox-group v-model="selectedCategories">
          <el-checkbox label="服裝">服裝</el-checkbox>
          <el-checkbox label="書籍">書籍</el-checkbox>
          <el-checkbox label="服務">服務</el-checkbox>
          <el-checkbox label="配件">配件</el-checkbox>
          <el-checkbox label="家具">家具</el-checkbox>
        </el-checkbox-group>
      </div>
      <el-divider />
      <div class="filter-group">
        <h4>價格範圍</h4>
        <el-slider
          v-model="priceRange"
          range
          :max="500"
          :marks="{0:'NT$0', 500:'NT$500', 1000:'NT$1000+'}"
          show-stops
        />
      </div>
      <el-divider />
      <div class="filter-buttons">
        <el-button type="primary" @click="applyFiltersAndCloseDrawer" class="filter-apply-btn">套用篩選</el-button>
        <el-button @click="clearFiltersAndCloseDrawer" class="filter-clear-btn">清除篩選</el-button>
      </div>
    </el-aside>

    <!-- Main content for Product List -->
    <el-main>
      <div class="main-content-wrapper">
        <el-row justify="space-between" align="middle" class="list-controls">
          <el-col :xs="12" :sm="12" :md="isSmallScreen ? 18 : 12">
            <h1 class="page-title">探索我們的商品</h1>
          </el-col>
          <el-col :xs="12" :sm="12" :md="isSmallScreen ? 6 : 12" class="controls-right">
            <el-button v-if="isSmallScreen" @click="drawerVisible = true" icon="Filter" circle class="filter-button-mobile" aria-label="篩選"></el-button>
            <el-select v-model="sortBy" placeholder="排序方式" class="sort-select">
              <el-option label="預設排序" value="default"></el-option>
              <el-option label="價格由低到高" value="price_asc"></el-option>
              <el-option label="價格由高到低" value="price_desc"></el-option>
              <el-option label="最新上架" value="newest"></el-option>
            </el-select>
          </el-col>
        </el-row>

        <el-divider />

        <div v-if="filteredProducts.length > 0" class="product-grid">
          <ProductCard
            v-for="product in paginatedProducts"
            :key="product.id"
            :product="product"
          />
        </div>
        <el-empty v-else description="目前沒有符合條件的商品">
          <el-button type="primary" @click="clearFilters">清除所有篩選條件</el-button>
        </el-empty>

        <el-row justify="center" class="pagination-container" v-if="filteredProducts.length > 0">
          <el-pagination
            background
            layout="prev, pager, next, jumper, ->, total"
            :total="filteredProducts.length"
            :page-size="pageSize"
            v-model:current-page="currentPage"
            @current-change="handlePageChange"
            :hide-on-single-page="true"
          />
        </el-row>
      </div>
    </el-main>

    <!-- Drawer for Filters -->
    <el-drawer
      v-model="drawerVisible"
      title="篩選條件"
      direction="ltr"
      :size="isSmallScreen ? '80%' : '280px'"
      class="filter-drawer"
      :with-header="true"
    >
      <div class="drawer-content">
        <div class="filter-group">
            <h4>分類</h4>
            <el-checkbox-group v-model="selectedCategories">
            <el-checkbox label="服裝">服裝</el-checkbox>
            <el-checkbox label="書籍">書籍</el-checkbox>
            <el-checkbox label="服務">服務</el-checkbox>
            <el-checkbox label="配件">配件</el-checkbox>
            <el-checkbox label="家具">家具</el-checkbox>
            </el-checkbox-group>
        </div>
        <el-divider />
        <div class="filter-group">
            <h4>價格範圍</h4>
            <el-slider
              v-model="priceRange"
              range
              :max="500"
              :marks="{0:'NT$0', 500:'NT$500', 1000:'NT$1000+'}"
              show-stops
            />
        </div>
        <el-divider />
        <div class="filter-buttons-drawer">
            <el-button type="primary" @click="applyFiltersAndCloseDrawer" style="width: 100%;">套用篩選</el-button>
            <el-button @click="clearFiltersAndCloseDrawer" style="width: 100%; margin-top: 10px; margin-left:0;">清除篩選</el-button>
        </div>
      </div>
    </el-drawer>
  </el-container>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, watchEffect } from 'vue';
import ProductCard from '@/components/product/ProductCard.vue';
import type { Product } from '@/types/product';
import { ElMessage } from 'element-plus';
import { useMediaQuery, useCssVar } from '@vueuse/core';
import { productImageMap } from '@/assets/images/ProductImageMaps';

// --- Responsive ---
const isSmallScreen = useMediaQuery('(max-width: 768px)');
const drawerVisible = ref(false);
const pageContainerRef = ref<HTMLElement | null>(null);

const gridColumns = ref(3);
const gridColumnsVar = useCssVar('--grid-columns', pageContainerRef, { initialValue: gridColumns.value.toString() });

watchEffect(() => {
  if (isSmallScreen.value) {
    gridColumns.value = 2;
  } else {
    gridColumns.value = 4; // PC View with sidebar: 4 columns
  }
  if (pageContainerRef.value) {
    gridColumnsVar.value = gridColumns.value.toString();
  }
});

// --- Data ---
const allProducts = ref<Product[]>([]);
const filteredProducts = ref<Product[]>([]);
const paginatedProducts = ref<Product[]>([]);

const selectedCategories = ref<string[]>([]);
const priceRange = ref<[number, number]>([0, 1000]);

const sortBy = ref<string>('default');

const currentPage = ref<number>(1);
const pageSize = ref<number>(12); // Changed to 12 to better suit 4 columns


// //如果後端啟用
// const fetchProducts = async () => {
//  try {
//    const response = await fetch("http://localhost:8000/products"); 
//    const stockData: { id: string; stock: number }[] = await response.json();

//  // 合併 stock 到 mockProducts
//    const updatedProducts = mockProducts.map(p => {
//      const backendStock = stockData.find(s => s.id === p.id)?.stock ?? p.stock;
//      return {
//        ...p,
//        stock: backendStock,
//        price: backendStock < 500 ? p.price + 10 : p.price
//      };
//    });

//    allProducts.value = updatedProducts;
//    applyFiltersAndSort();
//  } catch (error) {
//    console.error("無法取得庫存資料:", error);
//  }
// };

const fetchProducts = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/products");
    const productsFromBackend: any[] = await response.json(); // 先用 any[] 接收，再進行轉換
    
    console.log("從後端獲取的原始商品資料:", productsFromBackend); // 方便除錯

    const adjustedProducts: Product[] = productsFromBackend.map(p => ({
      id: String(p.id), 
      name: p.name,
      description: p.description || '',
      price: p.price,
      stock: p.stock, // *** 修復：使用正確的庫存欄位 p.stock 而非 p.sold ***
      // imageUrl: p.image_url, // *** 將後端的 'image_url' 映射到前端的 'imageUrl' ***
      imageUrl: productImageMap[p.name] ?? p.image_url ?? '',
      category: p.category_name, 
    }));

    const finalProducts = adjustedProducts.map(p => ({
      ...p,
      price: p.stock < 500 ? p.price + 10 : p.price,
    }));

    allProducts.value = finalProducts;
    console.log("處理後的 allProducts (已轉換欄位名稱):", allProducts.value); // 方便除錯
    applyFiltersAndSort();
  } catch (error) {
    console.error("無法取得商品資料:", error);
    ElMessage.error('無法加載商品資料，請稍後再試。');
    // 清空商品列表，避免顯示舊資料
    allProducts.value = [];
    filteredProducts.value = [];
    paginatedProducts.value = [];
  }
};


// --- Filtering Logic ---
const applyFiltersAndCloseDrawer = () => {
  applyFilters();
  if (isSmallScreen.value) {
    drawerVisible.value = false;
  }
};

const clearFiltersAndCloseDrawer = () => {
  clearFilters();
  if (isSmallScreen.value) {
    drawerVisible.value = false;
  }
};

const applyFilters = () => {
  currentPage.value = 1;
  applyFiltersAndSort();
  ElMessage.success('篩選已套用！');
};

const clearFilters = () => {
  selectedCategories.value = [];
  priceRange.value = [0, 1000];
  sortBy.value = 'default';
  currentPage.value = 1;
  applyFiltersAndSort();
  ElMessage.info('篩選已清除。');
};

// --- Sorting and Pagination Logic ---
const applyFiltersAndSort = () => {
  let productsToProcess = [...allProducts.value];
  if (selectedCategories.value.length > 0) {
    productsToProcess = productsToProcess.filter(p =>
      selectedCategories.value.includes(p.category ?? '')
  );

  }

  productsToProcess = productsToProcess.filter(p => p.price >= priceRange.value[0] && p.price <= priceRange.value[1]);

  switch (sortBy.value) {
    case 'price_asc':
      productsToProcess.sort((a, b) => a.price - b.price);
      break;
    case 'price_desc':
      productsToProcess.sort((a, b) => b.price - a.price);
      break;
    case 'newest':
      productsToProcess.sort((a, b) => parseInt(b.id) - parseInt(a.id)); // Example for newest
      break;
    default: // 'default'
      productsToProcess.sort((a,b) => parseInt(a.id) - parseInt(b.id));
      break;
  }
  filteredProducts.value = productsToProcess;
  updatePaginatedProducts();
};

const updatePaginatedProducts = () => {
  const start = (currentPage.value - 1) * pageSize.value;
  const end = start + pageSize.value;
  paginatedProducts.value = filteredProducts.value.slice(start, end);
};

const handlePageChange = (page: number) => {
  currentPage.value = page;
  updatePaginatedProducts();
};

watch(sortBy, () => {
    currentPage.value = 1;
    applyFiltersAndSort();
});

// --- Lifecycle Hooks ---
onMounted(() => {
  fetchProducts();
});
</script>

<style scoped>
/* Page Structure */
.product-list-page {
  background-color: var(--background-color);
  min-height: 100vh;
}

/* Sidebar Styling */
.filter-sidebar {
  padding: var(--spacing-xl);
  background-color: var(--background-light);
  border-right: 1px solid var(--border-color);
  overflow-y: auto;
  height: 100vh;
  position: sticky;
  top: 0;
}

.filter-sidebar h3 {
  font-size: var(--font-size-lg);
  color: var(--text-primary);
  margin-bottom: var(--spacing-lg);
  font-weight: var(--font-weight-semibold);
}

.filter-group {
  margin-bottom: var(--spacing-xl);
}

.filter-group h4 {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.filter-sidebar :deep(.el-checkbox-group .el-checkbox) {
  display: block;
  margin-bottom: var(--spacing-sm);
}

.filter-sidebar :deep(.el-checkbox__label) {
  color: var(--text-secondary);
  font-size: var(--font-size-sm);
}

.filter-sidebar :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.filter-sidebar :deep(.el-slider__runway) {
  background-color: var(--border-color);
}

.filter-sidebar :deep(.el-slider__bar) {
  background-color: var(--primary-color);
}

.filter-sidebar :deep(.el-slider__button) {
  border-color: var(--primary-color);
}

.filter-buttons {
  margin-top: var(--spacing-xl);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.filter-apply-btn,
.filter-clear-btn {
  width: 100%;
  border-radius: var(--border-radius);
  font-weight: var(--font-weight-medium);
}

.filter-apply-btn {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.filter-clear-btn {
  background-color: transparent;
  border-color: var(--border-color);
  color: var(--text-secondary);
}

/* Main Content */
.el-main {
  padding: var(--spacing-xl) var(--spacing-lg);
  background-color: var(--background-color);
}

.main-content-wrapper {
  max-width: var(--container-max-width);
  margin: 0 auto;
}

@media (min-width: 769px) {
  .el-main {
    padding: var(--spacing-xl) var(--spacing-xl);
  }
}

@media (min-width: 992px) {
  .el-main {
    padding: var(--spacing-xxl) var(--spacing-xl);
  }
}

@media (min-width: 1200px) {
  .el-main {
    padding: var(--spacing-xxl) var(--spacing-xxl);
  }
  .main-content-wrapper {
    max-width: 1440px;
  }
}

/* List Controls */
.list-controls {
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
}

.list-controls .el-col {
  display: flex;
  align-items: center;
}

.controls-right {
  justify-content: flex-end;
  gap: var(--spacing-md);
}

.filter-button-mobile {
  margin-right: var(--spacing-md);
  background-color: var(--surface-color);
  border-color: var(--border-color);
  color: var(--text-secondary);
}

.filter-button-mobile:hover {
  background-color: var(--primary-light);
  border-color: var(--primary-color);
  color: var(--primary-color);
}

.sort-select {
  min-width: 140px;
  max-width: 180px;
}

.sort-select :deep(.el-input__wrapper) {
  border-radius: var(--border-radius);
  border-color: var(--border-color);
}

.page-title {
  font-size: var(--font-size-xxl);
  color: var(--text-primary);
  font-weight: var(--font-weight-bold);
  margin: 0;
}

/* Product Grid */
.product-grid {
  display: grid;
  gap: var(--spacing-xl);
  grid-template-columns: repeat(1, 1fr);
  margin-bottom: var(--spacing-xl);
}

@media (min-width: 576px) {
  .product-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (min-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(var(--grid-columns, 2), 1fr);
  }
}

@media (min-width: 992px) {
  .product-grid {
    grid-template-columns: repeat(var(--grid-columns, 3), 1fr);
  }
}

@media (min-width: 1200px) {
  .product-grid {
    grid-template-columns: repeat(var(--grid-columns, 4), 1fr);
  }
}

/* Empty State */
.el-empty {
  margin: var(--spacing-xxl) auto;
  padding: var(--spacing-xl);
  background-color: var(--surface-color);
  border-radius: var(--border-radius-lg);
  border: 1px solid var(--border-color);
}

.el-empty :deep(.el-empty__description p) {
  color: var(--text-secondary);
  font-size: var(--font-size-md);
  margin-bottom: var(--spacing-lg);
}

.el-empty .el-button {
  font-size: var(--font-size-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  border-radius: var(--border-radius);
}

/* Pagination */
.pagination-container {
  margin-top: var(--spacing-xxl);
  padding-bottom: var(--spacing-lg);
}

.pagination-container :deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background-color: var(--primary-color);
  border-color: var(--primary-color);
}

.pagination-container :deep(.el-pagination.is-background .el-pager li:not(.is-disabled):hover) {
  color: var(--primary-color);
}

.pagination-container :deep(.el-pagination) {
  font-size: var(--font-size-sm);
}

/* Drawer Styles */
.filter-drawer :deep(.el-drawer__header) {
  margin-bottom: 0;
  padding: var(--spacing-lg) var(--spacing-lg);
  border-bottom: 1px solid var(--border-color);
  background-color: var(--surface-color);
}

.filter-drawer :deep(.el-drawer__title) {
  font-size: var(--font-size-lg);
  color: var(--text-primary);
  font-weight: var(--font-weight-semibold);
}

.filter-drawer .drawer-content {
  padding: var(--spacing-lg);
  overflow-y: auto;
  height: calc(100% - 60px);
  background-color: var(--background-light);
}

.filter-buttons-drawer {
  margin-top: var(--spacing-xl);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.filter-buttons-drawer .el-button {
  width: 100%;
  border-radius: var(--border-radius);
  font-weight: var(--font-weight-medium);
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-title {
    font-size: var(--font-size-xl);
  }
  
  .el-main {
    padding: var(--spacing-lg) var(--spacing-md);
  }
  
  .filter-button-mobile {
    padding: var(--spacing-sm);
    font-size: var(--font-size-sm);
  }
  
  .sort-select {
    min-width: 120px;
    font-size: var(--font-size-xs);
  }
  
  .list-controls {
    margin-bottom: var(--spacing-lg);
  }
  
  .product-grid {
    gap: var(--spacing-lg);
  }
}

@media (max-width: 576px) {
  .page-title {
    font-size: var(--font-size-lg);
  }
  
  .el-main {
    padding: var(--spacing-md) var(--spacing-sm);
  }
  
  .controls-right {
    gap: var(--spacing-sm);
  }
  
  .filter-drawer :deep(.el-slider__marks-text) {
    font-size: 10px !important;
  }
  
  .product-grid {
    gap: var(--spacing-md);
  }
}

/* Divider Styling */
.filter-sidebar :deep(.el-divider--horizontal) {
  margin: var(--spacing-lg) 0;
  border-color: var(--border-color);
}

.list-controls :deep(.el-divider--horizontal) {
  margin: var(--spacing-lg) 0;
  border-color: var(--border-color);
}
</style>