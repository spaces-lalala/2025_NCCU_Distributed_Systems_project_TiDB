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
const cartItemCount = computed(() => cartStore.cartItemCount);

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
  background-color: #ffffff;
  border-bottom: 1px solid #e0e0e0;
  padding: 0 20px; /* Add some horizontal padding */
}

.logo-link {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: #303133; /* Element Plus default text color */
  font-size: 20px;
  font-weight: bold;
}

.logo-image {
  height: 40px; /* Adjust as needed */
  margin-right: 10px;
}

.nav-menu {
  border-bottom: none; /* Remove default border from el-menu */
  display: flex;
  justify-content: flex-end; /* Align menu items to the right */
}

/* Ensure sub-menu items are also aligned if needed */
.el-menu--horizontal .el-menu .el-menu-item,
.el-menu--horizontal .el-menu .el-sub-menu__title {
  /* Adjust styling for sub-menu items if necessary */
}

.cart-badge {
  margin-left: 5px;
  transform: translateY(-2px); /* Fine-tune badge position */
}
</style> 