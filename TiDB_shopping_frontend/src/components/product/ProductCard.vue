<template>
  <router-link :to="`/product/${product.id}`" class="product-card-link">
    <el-card :body-style="{ padding: '0px' }" class="product-card" shadow="hover">
    <!-- SLOT: 放入排名徽章等額外內容 -->
      <slot />
      <img :src="product.imageUrl || defaultImage" class="product-image" @error="onImageError" />
      <div style="padding: 14px">
        <h3 class="product-name">{{ product.name }}</h3>
        <p class="product-description">{{ product.description }}</p>
        <div class="product-details">
          <span class="product-price">NT$ {{ product.price.toFixed(2) }}</span>
          <!-- You can add more details here, like stock, category, etc. -->
        </div>
        <div class="product-actions">
          <el-button type="warning" plain size="small" @click.prevent="addToCartHandler" :icon="ShoppingCart">加入購物車</el-button>
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

const addToCartHandler = () => {
  cartStore.addItem(props.product, 1);
  ElMessage.success(`${props.product.name} 已加入購物車`);
  emit('add-to-cart', props.product);
};

</script>

<style scoped>
.product-card-link {
  text-decoration: none;
  color: inherit;
  display: block;
}

.product-card {
  width: 100%;
  max-width: 300px;
  margin-bottom: 20px;
  transition: transform 0.2s ease-in-out;
  position: relative;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  display: block;
}

.product-name {
  font-size: 1.1em;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 8px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.product-details {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-size: 0.9em;
  color: #606266;
}

.product-price {
  font-size: 1.2em;
  font-weight: bold;
  color: #F56C6C;
}

.product-actions {
  display: flex;
  justify-content: flex-end;
  padding-top: 10px;
  border-top: 1px solid #ebeef5;
}
</style> 