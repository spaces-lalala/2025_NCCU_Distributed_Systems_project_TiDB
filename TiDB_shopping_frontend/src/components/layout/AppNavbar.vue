<template>
  <el-header class="app-navbar">
    <el-row justify="space-between" align="middle" style="height: 100%;">
      <el-col :span="6">
        <router-link to="/" class="logo-link">
          <!-- <img src="@/assets/images/logo.svg" alt="Logo" class="logo-image" /> -->
          <span>購物網站</span>
        </router-link>
      </el-col>
      <el-col :span="18">
        <el-menu mode="horizontal" :router="true" :ellipsis="false" class="nav-menu">
          <el-menu-item index="/">首頁</el-menu-item>
          <el-menu-item index="/products">商品列表</el-menu-item>
          <el-menu-item index="/bestsellers">熱銷排行</el-menu-item>
          <el-sub-menu index="/user-actions">
            <template #title>會員</template>
            <el-menu-item v-if="!isLoggedIn" index="/login">登入</el-menu-item>
            <el-menu-item v-if="!isLoggedIn" index="/register">註冊</el-menu-item>
            <el-menu-item v-if="isLoggedIn" index="/profile">會員中心</el-menu-item>
            <el-menu-item v-if="isLoggedIn" @click="handleLogout">登出</el-menu-item>
          </el-sub-menu>
          <el-menu-item index="/cart">
            <el-icon><ShoppingCart /></el-icon>
            購物車 <el-badge :value="cartItemCount" :hidden="cartItemCount === 0" class="cart-badge"></el-badge>
          </el-menu-item>
          <el-menu-item index="/admin">管理者後台</el-menu-item>
        </el-menu>
      </el-col>
    </el-row>
  </el-header>
</template>

<script lang="ts" setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { ShoppingCart } from '@element-plus/icons-vue'; // Import icons
import { useAuthStore } from '@/store/auth';
import { useCartStore } from '@/store/cart';

const router = useRouter();
const authStore = useAuthStore();
const cartStore = useCartStore();

const isLoggedIn = computed(() => authStore.isAuthenticated);
const cartItemCount = computed(() => cartStore.getTotalItemQuantity);

const handleLogout = () => {
  authStore.logout();
  ElMessage.success('已成功登出');
  router.push('/');
};

// Placeholder for logo - ensure you have a logo.svg in src/assets/images/
// or update the path accordingly.
</script>

<style scoped>
.app-navbar {
  background-color: var(--bg-color);
  border-bottom: 1px solid var(--border-light);
  padding: 0 var(--spacing-lg);
  box-shadow: var(--shadow-light);
  position: sticky;
  top: 0;
  z-index: 100;
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: var(--text-primary);
  font-size: var(--font-size-xl);
  font-weight: 700;
  transition: color 0.2s ease;
}

.logo-link:hover {
  color: var(--primary-color);
}

.logo-image {
  height: 40px;
  margin-right: var(--spacing-sm);
}

.nav-menu {
  border-bottom: none;
  display: flex;
  justify-content: flex-end;
  background-color: transparent;
}

.nav-menu .el-menu-item {
  font-weight: 500;
  color: var(--text-regular);
  border-bottom: 2px solid transparent;
  transition: all 0.2s ease;
}

.nav-menu .el-menu-item:hover {
  color: var(--primary-color);
  background-color: var(--bg-page);
}

.nav-menu .el-menu-item.is-active {
  color: var(--primary-color);
  border-bottom-color: var(--primary-color);
  background-color: transparent;
}

.cart-badge {
  margin-left: var(--spacing-xs);
  transform: translateY(-2px);
}

/* 響應式設計 */
@media (max-width: 768px) {
  .app-navbar {
    padding: 0 var(--spacing-md);
  }
  
  .logo-link {
    font-size: var(--font-size-lg);
  }
}
</style>