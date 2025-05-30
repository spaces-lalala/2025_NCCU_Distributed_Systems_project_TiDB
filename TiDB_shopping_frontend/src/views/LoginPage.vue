<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h2 class="login-title">使用者登入</h2>
        <p class="login-subtitle">歡迎回來！請登入您的帳號</p>
      </div>
      
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        label-width="0"
        class="login-form"
        @submit.prevent="submitForm"
      >
        <el-form-item prop="email">
          <el-input 
            v-model="loginForm.email" 
            type="email" 
            placeholder="請輸入 Email"
            size="large"
            prefix-icon="Message"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="loginForm.password" 
            type="password" 
            placeholder="請輸入密碼" 
            show-password
            size="large"
            prefix-icon="Lock"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button 
            type="primary" 
            native-type="submit" 
            :loading="isLoading" 
            class="login-button"
            size="large"
          >
            登入
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="login-footer">
        <router-link to="/register" class="register-link">
          還沒有帳號？立即註冊
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';
import { ElMessage } from 'element-plus';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/store/auth';
import { loginUser } from '@/services/authService';
import type { UserLoginData, AuthResponse } from '@/types/auth';

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const loginFormRef = ref<FormInstance>();
const isLoading = ref(false);

const loginForm = reactive<UserLoginData>({
  email: '',
  password: '',
});

const loginRules = reactive<FormRules>({
  email: [
    { required: true, message: '請輸入 Email', trigger: 'blur' },
    { type: 'email', message: '請輸入有效的 Email 地址', trigger: ['blur', 'change'] },
  ],
  password: [
    { required: true, message: '請輸入密碼', trigger: 'blur' },
  ],
});

const submitForm = async () => {
  if (!loginFormRef.value) return;
  await loginFormRef.value.validate(async (valid) => {
    if (valid) {
      isLoading.value = true;
      try {
        console.log('準備提交登入資料:', loginForm);
        const response: AuthResponse = await loginUser(loginForm);
        console.log('登入成功 API 回應 (模擬):', response);

        if (response.token && response.user) {
          authStore.setAuthState(response);
          ElMessage.success(response.message || '登入成功！');

          const redirectPath = route.query.redirect as string || '/';
          router.push(redirectPath);
        } else {
          throw new Error(response.message || '登入失敗：無效的回應格式。');
        }
      } catch (error: any) {
        console.error('登入失敗:', error);
        ElMessage.error(error.message || '登入失敗，請檢查您的帳號密碼或稍後再試。');
      } finally {
        isLoading.value = false;
      }
    } else {
      ElMessage.error('表單驗證失敗，請檢查輸入。');
      return false;
    }
  });
};
</script>

<style scoped>
.login-page {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
}

.login-container {
  width: 100%;
  max-width: 420px;
  background-color: var(--bg-color);
  border-radius: var(--border-radius-large);
  box-shadow: var(--shadow-dark);
  padding: var(--spacing-xxl);
  border: 1px solid var(--border-lighter);
}

.login-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.login-title {
  font-size: var(--font-size-xxl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.login-subtitle {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  margin-bottom: 0;
}

.login-form {
  margin-bottom: var(--spacing-lg);
}

.login-form .el-form-item {
  margin-bottom: var(--spacing-lg);
}

.login-form .el-input {
  border-radius: var(--border-radius-base);
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: var(--font-size-base);
  font-weight: 600;
  border-radius: var(--border-radius-base);
}

.login-footer {
  text-align: center;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-extra-light);
}

.register-link {
  color: var(--primary-color);
  font-size: var(--font-size-sm);
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s ease;
}

.register-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .login-page {
    padding: var(--spacing-md);
    align-items: flex-start;
    padding-top: var(--spacing-xxl);
  }
  
  .login-container {
    max-width: 100%;
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-light);
  }
  
  .login-title {
    font-size: var(--font-size-xl);
  }
}
</style>