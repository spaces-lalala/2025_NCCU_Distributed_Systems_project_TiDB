<template>
  <div class="register-page">
    <div class="register-container">
      <div class="register-header">
        <h2 class="register-title">使用者註冊</h2>
        <p class="register-subtitle">加入我們，享受優質購物體驗</p>
      </div>
      
      <el-form
        ref="registerFormRef"
        :model="registerForm"
        :rules="registerRules"
        label-width="0"
        class="register-form"
        @submit.prevent="submitForm"
      >
        <el-form-item prop="name">
          <el-input 
            v-model="registerForm.name" 
            placeholder="請輸入會員名稱"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="email">
          <el-input 
            v-model="registerForm.email" 
            type="email" 
            placeholder="請輸入 Email"
            size="large"
            prefix-icon="Message"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input 
            v-model="registerForm.password" 
            type="password" 
            placeholder="請輸入密碼"
            show-password
            size="large"
            prefix-icon="Lock"
          />
        </el-form-item>
        
        <el-form-item prop="confirmPassword">
          <el-input 
            v-model="registerForm.confirmPassword" 
            type="password" 
            placeholder="請確認密碼"
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
            class="register-button"
            size="large"
          >
            註冊
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="register-footer">
        <router-link to="/login" class="login-link">
          已有帳號？立即登入
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import type { FormInstance, FormRules } from 'element-plus';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router'; // Import useRouter
import { registerUser } from '@/services/authService';
import type { UserRegistrationData } from '@/types/auth';

const router = useRouter(); // Initialize router
const registerFormRef = ref<FormInstance>();
const isLoading = ref(false); // For loading state feedback

const registerForm = reactive<UserRegistrationData & { confirmPassword: string }>({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
});

const validatePass = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('請再次輸入密碼'));
  } else if (value !== registerForm.password) {
    callback(new Error("兩次輸入的密碼不一致!"));
  } else {
    callback();
  }
};

const registerRules = reactive<FormRules>({
  name: [
    { required: true, message: '請輸入會員名稱', trigger: 'blur' },
    { min: 2, message: '會員名稱長度不能少於 2 個字元', trigger: 'blur' },
  ],
  email: [
    { required: true, message: '請輸入 Email', trigger: 'blur' },
    { type: 'email', message: '請輸入有效的 Email 地址', trigger: ['blur', 'change'] },
  ],
  password: [
    { required: true, message: '請輸入密碼', trigger: 'blur' },
    { min: 6, message: '密碼長度不能少於 6 位', trigger: 'blur' },
  ],
  confirmPassword: [
    { required: true, message: '請確認密碼', trigger: 'blur' },
    { validator: validatePass, trigger: 'blur' },
  ],
});

const submitForm = async () => {
  if (!registerFormRef.value) return;
  await registerFormRef.value.validate(async (valid) => {
    if (valid) {
      isLoading.value = true;
      try {
        const userData: UserRegistrationData = {
          name: registerForm.name,
          email: registerForm.email,
          password: registerForm.password,
        };
        console.log('準備提交註冊資料:', userData);
        const response = await registerUser(userData);
        console.log('註冊成功 API 回應:', response);

        ElMessage.success(response.message || '註冊成功！將跳轉至登入頁面...');
        // Navigate to login page after successful registration
        // Assuming your login route is named 'Login' or path is '/login'
        await router.push({ name: 'Login' }); 
      } catch (error: any) {
        console.error('註冊失敗:', error);
        ElMessage.error(error.message || '註冊失敗，請稍後再試。');
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
.register-page {
  min-height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-lg);
}

.register-container {
  width: 100%;
  max-width: 450px;
  background-color: var(--bg-color);
  border-radius: var(--border-radius-large);
  box-shadow: var(--shadow-dark);
  padding: var(--spacing-xxl);
  border: 1px solid var(--border-lighter);
}

.register-header {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.register-title {
  font-size: var(--font-size-xxl);
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.register-subtitle {
  font-size: var(--font-size-base);
  color: var(--text-secondary);
  margin-bottom: 0;
}

.register-form {
  margin-bottom: var(--spacing-lg);
}

.register-form .el-form-item {
  margin-bottom: var(--spacing-lg);
}

.register-form .el-input {
  border-radius: var(--border-radius-base);
}

.register-button {
  width: 100%;
  height: 48px;
  font-size: var(--font-size-base);
  font-weight: 600;
  border-radius: var(--border-radius-base);
}

.register-footer {
  text-align: center;
  padding-top: var(--spacing-lg);
  border-top: 1px solid var(--border-extra-light);
}

.login-link {
  color: var(--primary-color);
  font-size: var(--font-size-sm);
  font-weight: 500;
  text-decoration: none;
  transition: color 0.2s ease;
}

.login-link:hover {
  color: var(--primary-dark);
  text-decoration: underline;
}

/* 響應式設計 */
@media (max-width: 768px) {
  .register-page {
    padding: var(--spacing-md);
    align-items: flex-start;
    padding-top: var(--spacing-xxl);
  }
  
  .register-container {
    max-width: 100%;
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-light);
  }
  
  .register-title {
    font-size: var(--font-size-xl);
  }
}
</style>