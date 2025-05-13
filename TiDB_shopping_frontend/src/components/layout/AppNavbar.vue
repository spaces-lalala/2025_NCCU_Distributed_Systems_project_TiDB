<template>
  <el-header class="app-navbar">
    <div class="logo-container">
      <router-link to="/">TiDB Shopping</router-link>
    </div>
    <el-menu mode="horizontal" :ellipsis="false" class="nav-menu">
      <el-menu-item index="1"><router-link to="/">Home</router-link></el-menu-item>
      <el-menu-item index="2"><router-link to="/products">Products</router-link></el-menu-item>
      <el-menu-item index="3"><router-link to="/cart">Cart</router-link></el-menu-item>
      <el-menu-item index="4"><router-link to="/profile">Profile</router-link></el-menu-item>
      <el-menu-item index="5"><router-link to="/login">Login</router-link></el-menu-item>
    </el-menu>
  </el-header>
</template>

<script setup lang="ts">
// No specific script needed for now
</script>

<style scoped>
.app-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--el-menu-border-color);
  padding: 0 20px;
}

.logo-container a {
  font-size: 1.5rem;
  font-weight: bold;
  text-decoration: none;
  color: var(--el-text-color-primary);
}

.nav-menu {
  border-bottom: none; /* Remove default border from el-menu */
}

.nav-menu .el-menu-item a {
  text-decoration: none;
  color: inherit; /* Ensure link color matches menu item color */
}

.nav-menu .el-menu-item.is-active a {
  color: var(--el-color-primary); /* Highlight active link */
}
</style> 