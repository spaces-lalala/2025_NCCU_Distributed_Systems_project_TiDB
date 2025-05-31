<template>
  <div class="manager-page">
    <!-- Header Section -->
    <div class="header-section">
      <div class="container">
        <h1 class="page-title">
          <el-icon class="title-icon"><DataAnalysis /></el-icon>
          管理者後台
        </h1>
        <p class="page-subtitle">系統數據分析與管理</p>
      </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
      <div class="container">
        <!-- Management Tabs -->
        <div class="management-section">
          <el-tabs v-model="activeTab" class="demo-tabs">
            <el-tab-pane label="數據分析" name="analytics">
              <div class="tab-content">
                <!-- Metabase Dashboard Embed -->
                <div class="dashboard-container">
                  <div class="dashboard-header">
                    <h3>
                      <el-icon><DataAnalysis /></el-icon>
                      整體銷售分析 Dashboard
                    </h3>
                    <el-button type="primary" @click="refreshDashboard">
                      <el-icon><Refresh /></el-icon>
                      重新載入
                    </el-button>
                  </div>
                  
                  <div class="dashboard-wrapper">
                    <el-loading 
                      :loading="dashboardLoading" 
                      text="載入 Dashboard 中..."
                      background="rgba(0, 0, 0, 0.8)"
                    >
                      <iframe
                        v-if="metabaseEmbedUrl"
                        :src="metabaseEmbedUrl"
                        frameborder="0"
                        class="dashboard-iframe"
                        allowtransparency
                        @load="onDashboardLoad"
                      ></iframe>
                      <div v-else class="dashboard-placeholder">
                        <el-icon class="placeholder-icon"><DataAnalysis /></el-icon>
                        <p>Dashboard 暫時無法載入</p>
                        <el-button type="primary" @click="loadDashboard">重試</el-button>
                      </div>
                    </el-loading>
                  </div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { DataAnalysis, Refresh } from '@element-plus/icons-vue'
import axios from 'axios'

// State
const activeTab = ref('analytics')
const metabaseEmbedUrl = ref('')
const dashboardLoading = ref(true)

// Methods
const loadDashboard = async () => {
  dashboardLoading.value = true
  try {
    // 向 Python FastAPI 後端請求嵌入用的 URL
    const res = await axios.get('http://localhost:8000/api/metabase_url')
    metabaseEmbedUrl.value = res.data.url
    ElMessage.success('Dashboard 載入成功')
  } catch (err) {
    console.error('無法載入 Metabase 嵌入連結', err)
    ElMessage.error('無法載入 Dashboard，請檢查後端服務')
  } finally {
    dashboardLoading.value = false
  }
}

const refreshDashboard = () => {
  ElMessage.info('重新載入 Dashboard...')
  loadDashboard()
}

const onDashboardLoad = () => {
  dashboardLoading.value = false
}

// Lifecycle
onMounted(() => {
  loadDashboard()
})
</script>

<style scoped>
/* 保留與 Dashboard 相關的樣式 */
.dashboard-container {
  background: #f8fafc;
  border-radius: 8px;
  overflow: hidden;
}

.dashboard-header {
  background: white;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.dashboard-header h3 {
  margin: 0;
  font-size: 1.125rem;
  font-weight: 600;
  color: #111827;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.dashboard-wrapper {
  position: relative;
  height: 600px;
  background: white;
}

.dashboard-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.dashboard-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #6b7280;
  gap: 1rem;
}

.placeholder-icon {
  font-size: 4rem;
  color: #d1d5db;
}
</style>