<template>
  <div class="register-page">
    <h2>使用者註冊</h2>
    <el-form
      ref="registerFormRef"
      :model="registerForm"
      :rules="registerRules"
      label-width="120px"
      class="register-form"
      @submit.prevent="submitForm"
    >
      <el-form-item label="會員名稱" prop="name">
        <el-input v-model="registerForm.name" />
      </el-form-item>
      <el-form-item label="Email" prop="email">
        <el-input v-model="registerForm.email" type="email" />
      </el-form-item>
      <el-form-item label="密碼" prop="password">
        <el-input v-model="registerForm.password" type="password" show-password />
      </el-form-item>
      <el-form-item label="確認密碼" prop="confirmPassword">
        <el-input v-model="registerForm.confirmPassword" type="password" show-password />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" native-type="submit" :loading="isLoading">註冊</el-button>
      </el-form-item>
    </el-form>
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
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
}

.register-form {
  width: 100%;
  max-width: 400px;
  margin-top: 20px;
}
</style> 