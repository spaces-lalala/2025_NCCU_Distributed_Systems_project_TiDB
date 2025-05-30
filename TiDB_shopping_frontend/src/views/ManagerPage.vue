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
        <!-- Statistics Cards -->
        <div class="stats-grid">
          <div class="stat-card sales">
            <div class="stat-icon">
              <el-icon><TrendCharts /></el-icon>
            </div>
            <div class="stat-content">
              <h3>總銷售額</h3>
              <p class="stat-value">$123,456</p>
              <span class="stat-change positive">+12.5%</span>
            </div>
          </div>
          
          <div class="stat-card orders">
            <div class="stat-icon">
              <el-icon><Document /></el-icon>
            </div>
            <div class="stat-content">
              <h3>總訂單數</h3>
              <p class="stat-value">1,234</p>
              <span class="stat-change positive">+8.3%</span>
            </div>
          </div>
          
          <div class="stat-card products">
            <div class="stat-icon">
              <el-icon><Box /></el-icon>
            </div>
            <div class="stat-content">
              <h3>商品總數</h3>
              <p class="stat-value">567</p>
              <span class="stat-change neutral">-</span>
            </div>
          </div>
          
          <div class="stat-card users">
            <div class="stat-icon">
              <el-icon><User /></el-icon>
            </div>
            <div class="stat-content">
              <h3>用戶總數</h3>
              <p class="stat-value">2,345</p>
              <span class="stat-change positive">+15.2%</span>
            </div>
          </div>
        </div>

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
              <el-tab-pane label="商品管理" name="products">
              <div class="tab-content">
                <div class="management-actions">
                  <el-button type="primary" @click="addProduct">
                    <el-icon><Plus /></el-icon>
                    新增商品
                  </el-button>
                  <el-button @click="exportProducts">
                    <el-icon><Download /></el-icon>
                    匯出數據
                  </el-button>
                  <el-button @click="loadProducts" :loading="productsLoading">
                    <el-icon><Refresh /></el-icon>
                    重新載入
                  </el-button>
                  <el-button @click="showBulkUpdateDialog = true" type="warning">
                    <el-icon><Edit /></el-icon>
                    批量更新庫存
                  </el-button>
                </div>
                
                <!-- 庫存預警 -->
                <div v-if="lowStockProducts.length > 0 || outOfStockProducts.length > 0" class="stock-alerts">
                  <el-alert title="庫存預警" type="warning" :closable="false" class="alert-header">
                    <template #default>
                      <div class="alert-content">
                        <span v-if="outOfStockProducts.length > 0">
                          🚨 {{ outOfStockProducts.length }} 個商品已缺貨
                        </span>
                        <span v-if="lowStockProducts.length > 0" class="low-stock-text">
                          ⚠️ {{ lowStockProducts.length }} 個商品庫存不足
                        </span>
                      </div>
                    </template>
                  </el-alert>
                </div>

                <!-- 商品列表 -->
                <div class="products-table-container">
                  <el-table
                    :data="paginatedProducts"
                    stripe
                    border
                    style="width: 100%"
                    v-loading="productsLoading"
                    element-loading-text="載入商品資料中..."
                  >
                    <el-table-column prop="id" label="商品ID" width="80" />
                    <el-table-column prop="name" label="商品名稱" min-width="200" />
                    <el-table-column prop="price" label="價格" width="100">
                      <template #default="{ row }">
                        NT$ {{ Number(row.price).toFixed(2) }}
                      </template>
                    </el-table-column>
                    <el-table-column prop="stock" label="庫存數量" width="120">
                      <template #default="{ row }">
                        <el-tag 
                          :type="getStockTagType(row.stock)" 
                          :effect="row.stock <= 0 ? 'dark' : 'light'"
                        >
                          {{ row.stock }} 件
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column prop="sold" label="已售數量" width="100" />
                    <el-table-column prop="category_name" label="分類" width="100" />
                    <el-table-column label="庫存狀態" width="100">
                      <template #default="{ row }">
                        <el-tag 
                          v-if="row.stock <= 0" 
                          type="danger" 
                          effect="dark"
                        >
                          已缺貨
                        </el-tag>
                        <el-tag 
                          v-else-if="row.stock <= 10" 
                          type="warning"
                        >
                          庫存不足
                        </el-tag>
                        <el-tag 
                          v-else 
                          type="success"
                        >
                          充足
                        </el-tag>
                      </template>
                    </el-table-column>
                    <el-table-column label="操作" width="200" fixed="right">
                      <template #default="{ row }">
                        <el-button 
                          size="small" 
                          @click="editStock(row)"
                          type="primary"
                          plain
                        >
                          編輯庫存
                        </el-button>
                        <el-button 
                          size="small" 
                          @click="viewProduct(row)"
                          type="info"
                          plain
                        >
                          查看詳情
                        </el-button>
                      </template>
                    </el-table-column>
                  </el-table>
                  
                  <!-- 分頁 -->
                  <div class="pagination-container">
                    <el-pagination
                      v-model:current-page="currentPage"
                      v-model:page-size="pageSize"
                      :page-sizes="[10, 20, 50, 100]"
                      :total="allProducts.length"
                      layout="total, sizes, prev, pager, next, jumper"
                      @size-change="handleSizeChange"
                      @current-change="handleCurrentChange"
                    />
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="訂單管理" name="orders">
              <div class="tab-content">
                <div class="management-actions">
                  <el-button type="primary" @click="viewAllOrders">
                    <el-icon><View /></el-icon>
                    查看所有訂單
                  </el-button>
                  <el-button @click="exportOrders">
                    <el-icon><Download /></el-icon>
                    匯出訂單
                  </el-button>
                </div>
                <div class="coming-soon">
                  <el-icon class="coming-soon-icon"><ShoppingCart /></el-icon>
                  <h3>訂單管理功能</h3>
                  <p>此功能正在開發中，敬請期待</p>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="用戶管理" name="users">
              <div class="tab-content">
                <div class="management-actions">
                  <el-button type="primary" @click="viewAllUsers">
                    <el-icon><User /></el-icon>
                    查看所有用戶
                  </el-button>
                  <el-button @click="exportUsers">
                    <el-icon><Download /></el-icon>
                    匯出用戶數據
                  </el-button>
                </div>
                <div class="coming-soon">
                  <el-icon class="coming-soon-icon"><UserFilled /></el-icon>
                  <h3>用戶管理功能</h3>
                  <p>此功能正在開發中，敬請期待</p>
                </div>
              </div>
            </el-tab-pane>          </el-tabs>
        </div>
      </div>
    </div>

    <!-- 編輯庫存對話框 -->
    <el-dialog 
      v-model="editStockDialog" 
      title="編輯商品庫存" 
      width="500px"
      :before-close="handleCloseEditDialog"
    >
      <el-form 
        :model="editingProduct" 
        label-width="100px" 
        v-if="editingProduct"
      >
        <el-form-item label="商品名稱">
          <el-input v-model="editingProduct.name" readonly />
        </el-form-item>
        <el-form-item label="當前庫存">
          <el-tag :type="getStockTagType(editingProduct.stock)">
            {{ editingProduct.stock }} 件
          </el-tag>
        </el-form-item>
        <el-form-item label="新庫存數量">
          <el-input-number 
            v-model="newStockValue" 
            :min="0" 
            :max="99999" 
            controls-position="right"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="變更原因">
          <el-input 
            v-model="stockChangeReason" 
            type="textarea" 
            placeholder="請輸入庫存變更原因（可選）"
            :rows="3"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="editStockDialog = false">取消</el-button>
          <el-button type="primary" @click="updateStock" :loading="updateStockLoading">
            確認更新
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 批量更新庫存對話框 -->
    <el-dialog 
      v-model="showBulkUpdateDialog" 
      title="批量更新庫存" 
      width="80%"
      :before-close="handleCloseBulkDialog"
    >
      <div class="bulk-update-container">
        <div class="bulk-actions">
          <el-button @click="selectAllProducts">全選</el-button>
          <el-button @click="unselectAllProducts">取消全選</el-button>
          <el-button @click="selectLowStockProducts">選擇庫存不足商品</el-button>
          <el-button @click="selectOutOfStockProducts">選擇缺貨商品</el-button>
        </div>
        
        <el-table
          ref="bulkTable"
          :data="allProducts"
          @selection-change="handleBulkSelectionChange"
          style="width: 100%"
          max-height="400"
        >
          <el-table-column type="selection" width="55" />
          <el-table-column prop="name" label="商品名稱" min-width="200" />
          <el-table-column prop="stock" label="當前庫存" width="120">
            <template #default="{ row }">
              <el-tag :type="getStockTagType(row.stock)">
                {{ row.stock }} 件
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="新庫存數量" width="150">
            <template #default="{ row, $index }">
              <el-input-number 
                v-model="bulkStockUpdates[row.id]" 
                :min="0" 
                :max="99999" 
                size="small"
                controls-position="right"
                style="width: 100%"
                :placeholder="row.stock.toString()"
              />
            </template>
          </el-table-column>
        </el-table>
      </div>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showBulkUpdateDialog = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="performBulkUpdate" 
            :loading="bulkUpdateLoading"
            :disabled="bulkSelectedProducts.length === 0"
          >
            批量更新 ({{ bulkSelectedProducts.length }} 個商品)
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  DataAnalysis, 
  TrendCharts, 
  Document, 
  Box, 
  User, 
  Refresh, 
  Plus, 
  Download, 
  Tools, 
  View, 
  ShoppingCart, 
  UserFilled,
  Edit
} from '@element-plus/icons-vue'
import axios from 'axios'

// Types
interface Product {
  id: number
  name: string
  price: number
  stock: number
  sold: number
  category_name: string
  description?: string
  image_url?: string
}

// State
const activeTab = ref('analytics')
const metabaseEmbedUrl = ref('')
const dashboardLoading = ref(true)

// Products management state
const allProducts = ref<Product[]>([])
const productsLoading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)

// Stock editing state
const editStockDialog = ref(false)
const editingProduct = ref<Product | null>(null)
const newStockValue = ref(0)
const stockChangeReason = ref('')
const updateStockLoading = ref(false)

// Bulk update state
const showBulkUpdateDialog = ref(false)
const bulkSelectedProducts = ref<Product[]>([])
const bulkStockUpdates = ref<Record<number, number>>({})
const bulkUpdateLoading = ref(false)
const bulkTable = ref()

// Computed
const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return allProducts.value.slice(start, end)
})

const lowStockProducts = computed(() => {
  return allProducts.value.filter(p => p.stock > 0 && p.stock <= 10)
})

const outOfStockProducts = computed(() => {
  return allProducts.value.filter(p => p.stock <= 0)
})

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

// Products management
const loadProducts = async () => {
  productsLoading.value = true
  try {
    const response = await axios.get('http://localhost:8000/api/admin/products')
    allProducts.value = response.data
    ElMessage.success(`載入了 ${allProducts.value.length} 個商品`)
  } catch (error) {
    console.error('載入商品失敗:', error)
    ElMessage.error('載入商品列表失敗')
  } finally {
    productsLoading.value = false
  }
}

const getStockTagType = (stock: number) => {
  if (stock <= 0) return 'danger'
  if (stock <= 10) return 'warning'
  return 'success'
}

const editStock = (product: Product) => {
  editingProduct.value = { ...product }
  newStockValue.value = product.stock
  stockChangeReason.value = ''
  editStockDialog.value = true
}

const viewProduct = (product: Product) => {
  ElMessageBox.alert(
    `商品名稱: ${product.name}\n價格: NT$ ${product.price}\n庫存: ${product.stock} 件\n已售: ${product.sold} 件\n分類: ${product.category_name}`,
    '商品詳情',
    {
      confirmButtonText: '確定',
      type: 'info'
    }
  )
}

const updateStock = async () => {
  if (!editingProduct.value) return
  
  updateStockLoading.value = true
  try {
    await axios.put(`http://localhost:8000/api/admin/products/${editingProduct.value.id}/stock`, null, {
      params: {
        new_stock: newStockValue.value
      }
    })
    
    // 更新本地數據
    const index = allProducts.value.findIndex(p => p.id === editingProduct.value!.id)
    if (index !== -1) {
      allProducts.value[index].stock = newStockValue.value
    }
    
    ElMessage.success('庫存更新成功')
    editStockDialog.value = false
  } catch (error) {
    console.error('更新庫存失敗:', error)
    ElMessage.error('更新庫存失敗')
  } finally {
    updateStockLoading.value = false
  }
}

const handleCloseEditDialog = () => {
  editStockDialog.value = false
  editingProduct.value = null
  newStockValue.value = 0
  stockChangeReason.value = ''
}

// Bulk operations
const handleBulkSelectionChange = (selection: Product[]) => {
  bulkSelectedProducts.value = selection
}

const selectAllProducts = () => {
  bulkTable.value?.toggleAllSelection()
}

const unselectAllProducts = () => {
  bulkTable.value?.clearSelection()
}

const selectLowStockProducts = () => {
  bulkTable.value?.clearSelection()
  lowStockProducts.value.forEach(product => {
    bulkTable.value?.toggleRowSelection(product, true)
  })
}

const selectOutOfStockProducts = () => {
  bulkTable.value?.clearSelection()
  outOfStockProducts.value.forEach(product => {
    bulkTable.value?.toggleRowSelection(product, true)
  })
}

const performBulkUpdate = async () => {
  if (bulkSelectedProducts.value.length === 0) {
    ElMessage.warning('請選擇要更新的商品')
    return
  }

  const updates = bulkSelectedProducts.value
    .filter(product => bulkStockUpdates.value[product.id] !== undefined)
    .map(product => ({
      product_id: product.id,
      stock: bulkStockUpdates.value[product.id]
    }))

  if (updates.length === 0) {
    ElMessage.warning('請設置要更新的庫存數量')
    return
  }

  bulkUpdateLoading.value = true
  try {
    await axios.post('http://localhost:8000/api/admin/products/bulk-update-stock', updates)
    
    // 更新本地數據
    updates.forEach(update => {
      const index = allProducts.value.findIndex(p => p.id === update.product_id)
      if (index !== -1) {
        allProducts.value[index].stock = update.stock
      }
    })
    
    ElMessage.success(`成功批量更新 ${updates.length} 個商品的庫存`)
    showBulkUpdateDialog.value = false
    bulkStockUpdates.value = {}
  } catch (error) {
    console.error('批量更新失敗:', error)
    ElMessage.error('批量更新庫存失敗')
  } finally {
    bulkUpdateLoading.value = false
  }
}

const handleCloseBulkDialog = () => {
  showBulkUpdateDialog.value = false
  bulkSelectedProducts.value = []
  bulkStockUpdates.value = {}
}

// Pagination
const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

// Management actions placeholders
const addProduct = () => {
  ElMessage.info('新增商品功能開發中...')
}

const exportProducts = () => {
  ElMessage.info('匯出商品數據功能開發中...')
}

const viewAllOrders = () => {
  ElMessage.info('查看所有訂單功能開發中...')
}

const exportOrders = () => {
  ElMessage.info('匯出訂單功能開發中...')
}

const viewAllUsers = () => {
  ElMessage.info('查看所有用戶功能開發中...')
}

const exportUsers = () => {
  ElMessage.info('匯出用戶數據功能開發中...')
}

// Lifecycle
onMounted(() => {
  loadDashboard()
  loadProducts()
})
</script>

<style scoped>
.manager-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.header-section {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 2rem 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

.page-title {
  color: white;
  font-size: 2.5rem;
  font-weight: 700;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.title-icon {
  font-size: 2.5rem;
}

.page-subtitle {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1.125rem;
  margin: 0.5rem 0 0 0;
  font-weight: 300;
}

.main-content {
  padding: 2rem 0;
}

/* Statistics Cards */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
}

.stat-card.sales {
  border-left: 4px solid #10b981;
}

.stat-card.orders {
  border-left: 4px solid #3b82f6;
}

.stat-card.products {
  border-left: 4px solid #f59e0b;
}

.stat-card.users {
  border-left: 4px solid #8b5cf6;
}

.stat-icon {
  flex-shrink: 0;
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.sales .stat-icon {
  background: linear-gradient(135deg, #10b981, #065f46);
}

.orders .stat-icon {
  background: linear-gradient(135deg, #3b82f6, #1e3a8a);
}

.products .stat-icon {
  background: linear-gradient(135deg, #f59e0b, #92400e);
}

.users .stat-icon {
  background: linear-gradient(135deg, #8b5cf6, #5b21b6);
}

.stat-content h3 {
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-value {
  margin: 0 0 0.25rem 0;
  font-size: 1.875rem;
  font-weight: 700;
  color: #111827;
}

.stat-change {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.5rem;
  border-radius: 6px;
}

.stat-change.positive {
  color: #10b981;
  background: #d1fae5;
}

.stat-change.negative {
  color: #ef4444;
  background: #fee2e2;
}

.stat-change.neutral {
  color: #6b7280;
  background: #f3f4f6;
}

/* Management Section */
.management-section {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.demo-tabs {
  --el-tabs-header-height: 60px;
}

.demo-tabs :deep(.el-tabs__header) {
  background: #f8fafc;
  margin: 0;
  border-bottom: 1px solid #e5e7eb;
}

.demo-tabs :deep(.el-tabs__nav) {
  padding: 0 1rem;
}

.demo-tabs :deep(.el-tabs__item) {
  height: 60px;
  line-height: 60px;
  font-weight: 600;
  color: #6b7280;
}

.demo-tabs :deep(.el-tabs__item.is-active) {
  color: #3b82f6;
}

.tab-content {
  padding: 2rem;
}

/* Dashboard Section */
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

/* Management Actions */
.management-actions {
  margin-bottom: 2rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

/* Stock Alerts */
.stock-alerts {
  margin-bottom: 2rem;
}

.alert-header {
  margin-bottom: 1rem;
}

.alert-content {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.low-stock-text {
  margin-left: 1rem;
}

/* Products Table */
.products-table-container {
  background: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.pagination-container {
  margin-top: 2rem;
  display: flex;
  justify-content: center;
}

/* Dialog Styles */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
}

.bulk-update-container {
  max-height: 500px;
  overflow-y: auto;
}

.bulk-actions {
  margin-bottom: 1rem;
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  padding: 1rem;
  background: #f5f7fa;
  border-radius: 6px;
}

.coming-soon {
  text-align: center;
  padding: 3rem 1rem;
  color: #6b7280;
}

.coming-soon-icon {
  font-size: 4rem;
  color: #d1d5db;
  margin-bottom: 1rem;
}

.coming-soon h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.25rem;
  font-weight: 600;
}

.coming-soon p {
  margin: 0;
  font-size: 1rem;
}

/* Responsive Design */
@media (max-width: 768px) {
  .page-title {
    font-size: 2rem;
  }
  
  .stats-grid {
    grid-template-columns: 1fr;
  }
  
  .stat-card {
    padding: 1rem;
  }
  
  .tab-content {
    padding: 1rem;
  }
  
  .dashboard-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
  }
  
  .management-actions {
    flex-direction: column;
  }
  
  .dashboard-wrapper {
    height: 400px;
  }
}

@media (max-width: 480px) {
  .container {
    padding: 0 0.5rem;
  }
  
  .main-content {
    padding: 1rem 0;
  }
  
  .stats-grid {
    gap: 1rem;
  }
  
  .stat-card {
    flex-direction: column;
    text-align: center;
  }
}

/* Loading animation */
.el-loading-mask {
  border-radius: 8px;
}

/* Custom button styles */
.el-button {
  border-radius: 8px;
  font-weight: 600;
}

.el-button--primary {
  background: linear-gradient(135deg, #3b82f6, #1e40af);
  border: none;
}

.el-button--primary:hover {
  background: linear-gradient(135deg, #1e40af, #1e3a8a);
}
</style>
