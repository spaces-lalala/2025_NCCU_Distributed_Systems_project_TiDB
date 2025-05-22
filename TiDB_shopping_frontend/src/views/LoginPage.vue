<template>
  <div class="login-page">
    <h2>使用者登入</h2>
    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      label-width="100px"
      class="login-form"
      @submit.prevent="submitForm"
    >
      <el-form-item label="Email" prop="email">
        <el-input v-model="loginForm.email" type="email" placeholder="請輸入 Email" />
      </el-form-item>
      <el-form-item label="密碼" prop="password">
        <el-input v-model="loginForm.password" type="password" placeholder="請輸入密碼" show-password />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit" :loading="isLoading" class="login-button">登入</el-button>
      </el-form-item>
    </el-form>
    <div class="links">
      <router-link to="/register">還沒有帳號？前往註冊</router-link>
      <!-- Add link to password reset if needed later -->
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
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px;
  min-height: calc(100vh - 120px); /* Adjust based on header/footer height */
}

.login-form {
  width: 100%;
  max-width: 360px;
  padding: 30px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  text-align: center;
  color: #333;
}

.login-button {
  width: 100%;
}

.links {
  margin-top: 20px;
  text-align: center;
}

.links a {
  color: var(--el-color-primary);
  text-decoration: none;
}

.links a:hover {
  text-decoration: underline;
}
</style> 