<template>
  <el-card :body-style="{ padding: '0px' }" class="product-card" shadow="hover">
    <img :src="product.image_url || defaultImage" class="product-image" @error="onImageError" />
    <div style="padding: 14px">
      <h3 class="product-name">{{ product.name }}</h3>
      <div class="product-details">
        <span class="product-price">￥{{ product.price.toFixed(2) }}</span>
        <!-- You can add more details here, like stock, category, etc. -->
      </div>
      <div class="product-actions">
        <el-button type="primary" plain size="small" @click="viewDetails">查看詳情</el-button>
        <el-button type="warning" plain size="small" @click="addToCart" :icon="ShoppingCart">加入購物車</el-button>
      </div>
    </div>
  </el-card>
</template>

<script lang="ts" setup>
import { defineProps, defineEmits } from 'vue';
import { ElMessage } from 'element-plus';
import { ShoppingCart } from '@element-plus/icons-vue';
import { useCartStore } from '@/store/cart';
import type { Product } from '@/types/domain'; // Assuming Product type is defined in domain.ts

// Props definition
interface Props {
  product: Product;
}
const props = defineProps<Props>();

// Emits definition
const emit = defineEmits<{
  (e: 'view-details', productId: string | number): void;
  (e: 'add-to-cart', product: Product): void;
}>();

const cartStore = useCartStore();

// Placeholder image if product image fails to load or is not provided
const defaultImage = 'https://via.placeholder.com/400x300.png?text=No+Image';

const onImageError = (event: Event) => {
  const imgElement = event.target as HTMLImageElement;
  imgElement.src = defaultImage;
};

const viewDetails = () => {
  emit('view-details', props.product.id);
};

const addToCart = () => {
  cartStore.addItem(props.product, 1); // Add 1 unit of the product
  ElMessage.success(`${props.product.name} 已加入購物車`);
  emit('add-to-cart', props.product);
};

</script>

<style scoped>
.product-card {
  width: 100%; /* Make card take full width of its container */
  max-width: 300px; /* Optional: Set a max-width for consistency */
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.product-card:hover {
  transform: translateY(-5px);
}

.product-image {
  width: 100%;
  height: 200px; /* Fixed height for images */
  object-fit: cover; /* Cover the area, might crop */
  /* Alternatively, use object-fit: contain; if you want to see the whole image */
  display: block;
}

.product-name {
  font-size: 1.1em;
  font-weight: 600;
  margin-top: 0;
  margin-bottom: 8px;
  white-space: nowrap; /* Prevent name from wrapping */
  overflow: hidden;
  text-overflow: ellipsis; /* Add ellipsis if name is too long */
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
  color: #F56C6C; /* Element Plus danger color for price */
}

.product-actions {
  display: flex;
  justify-content: space-between;
  padding-top: 10px;
  border-top: 1px solid #ebeef5; /* Element Plus divider color */
}
</style> 