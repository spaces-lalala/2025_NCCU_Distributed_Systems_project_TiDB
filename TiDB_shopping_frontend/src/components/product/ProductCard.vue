<template>
  <router-link :to="`/product/${product.id}`" class="product-card-link">
    <el-card :body-style="{ padding: '0px' }" class="product-card" shadow="hover">
    <!-- SLOT: 放入排名徽章等額外內容 -->
      <slot />      <div class="product-image-container">
        <img :src="product.imageUrl || defaultImage" class="product-image" @error="onImageError" />
      </div>
      <div class="product-content">
        <div class="product-info">
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-description">{{ product.description }}</p>
          <div class="product-price">NT$ {{ (product.price || 0).toFixed(2) }}</div>
        </div>
        <div class="product-actions">
          <el-button type="primary" plain size="small" @click.prevent="addToCartHandler" :icon="ShoppingCart">加入購物車</el-button>
        </div>
      </div>
    </el-card>
  </router-link>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits } from 'vue';
import { ElMessage } from 'element-plus';
import { ShoppingCart } from '@element-plus/icons-vue';
import { useCartStore } from '@/store/cart';
import type { Product } from '@/types/product';

// Props definition
interface Props {
  product: Product;
}
const props = defineProps<Props>();

// Emits definition
const emit = defineEmits<{
  (e: 'add-to-cart', product: Product): void;
}>();

const cartStore = useCartStore();

// Placeholder image if product image fails to load or is not provided
const defaultImage = 'https://via.placeholder.com/400x300.png?text=No+Image';

const onImageError = (event: Event) => {
  const imgElement = event.target as HTMLImageElement;
  imgElement.src = defaultImage;
};

const addToCartHandler = async () => {
  try {
    const result = await cartStore.addItem(props.product, 1);
    if (result.success) {
      ElMessage.success(result.message || `${props.product.name} 已加入購物車`);
      emit('add-to-cart', props.product);
    } else {
      ElMessage.error(result.message || '加入購物車失敗');
    }
  } catch (error) {
    console.error('加入購物車時發生錯誤:', error);
    ElMessage.error('加入購物車失敗，請稍後再試');
  }
};

</script>

<style scoped>
.product-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
  height: 100%;
}

.product-card {
  width: 100%;
  height: 100%;
  border: 1px solid var(--border-lighter);
  border-radius: var(--border-radius-base);
  overflow: hidden;
  transition: all 0.3s ease;
  box-shadow: var(--shadow-light);
  background-color: var(--bg-color);
  display: flex;
  flex-direction: column;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-base);
  border-color: var(--primary-color);
}

.product-image-container {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background-color: var(--bg-page);
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image {
  transform: scale(1.05);
}

.product-content {
  padding: var(--spacing-lg);
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.product-info {
  flex-grow: 1;
  margin-bottom: var(--spacing-md);
}

.product-name {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0 0 var(--spacing-sm) 0;
  line-height: 1.4;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.product-description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: 0 0 var(--spacing-md) 0;
  line-height: 1.5;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.product-price {
  font-size: var(--font-size-xl);
  font-weight: var(--font-weight-bold);
  color: var(--primary-color);
  margin-bottom: var(--spacing-md);
}

.product-actions {
  padding-top: var(--spacing-md);
  border-top: 1px solid var(--border-lighter);
  display: flex;
  justify-content: center;
  margin-top: auto;
}

.product-actions .el-button {
  width: 100%;
  font-weight: var(--font-weight-medium);
  border-radius: var(--border-radius-base);
  transition: var(--transition-base);
}

.product-actions .el-button:hover {
  transform: translateY(-1px);
}

/* Responsive Design */
@media (max-width: 768px) {
  .product-image-container {
    height: 160px;
  }
  
  .product-content {
    padding: var(--spacing-md);
  }
  
  .product-name {
    font-size: var(--font-size-base);
  }
  
  .product-price {
    font-size: var(--font-size-lg);
  }
}

@media (max-width: 576px) {
  .product-image-container {
    height: 140px;
  }
  
  .product-content {
    padding: var(--spacing-sm);
  }
  
  .product-actions .el-button {
    font-size: var(--font-size-xs);
    padding: var(--spacing-xs) var(--spacing-sm);
  }
}
</style>