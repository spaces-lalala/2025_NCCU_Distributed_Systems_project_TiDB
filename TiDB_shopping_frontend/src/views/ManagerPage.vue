<template>
  <div class="p-6">
    <!-- 圓餅圖 -->
    <h2 class="text-xl font-bold mb-4">產品銷售佔比</h2>
    <div ref="chartRef" style="width: 100%; height: 400px;" class="mb-12" />

    <!-- 購買記錄表格 -->
    <h2 class="text-xl font-bold mb-4">購買記錄</h2>
    <el-table :data="purchaseLog" stripe>
      <el-table-column prop="time" label="購買時間" width="180" />
      <el-table-column label="購買商品">
        <template #default="{ row }">
          <ul>
            <li v-for="(item, index) in row.products" :key="index">
              {{ item.product_name }} × {{ item.quantity }}
            </li>
          </ul>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

const salesReport = ref([])
const purchaseLog = ref([])
const chartRef = ref(null)
let chartInstance = null

// 渲染圓餅圖
const renderChart = () => {
  if (!chartRef.value || salesReport.value.length === 0) return

  const pieData = salesReport.value.map(item => ({
    name: item.product_name,
    value: item.total_sold
  }))

  if (!chartInstance) {
    chartInstance = echarts.init(chartRef.value)
  }

  chartInstance.setOption({
    title: {
      text: '產品銷售佔比',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {d}%'
    },
    legend: {
      bottom: 0,
      left: 'center'
    },
    series: [
      {
        name: '銷售量',
        type: 'pie',
        radius: '50%',
        data: pieData,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  })
}

onMounted(async () => {
  try {
    const token = localStorage.getItem('token')

    // 同時取得兩份資料
    const [salesRes, logRes] = await Promise.all([
      axios.get('/api/admin/sales_report', {
        headers: { Authorization: `Bearer ${token}` }
      }),
      axios.get('/api/admin/purchase_log', {
        headers: { Authorization: `Bearer ${token}` }
      })
    ])

    salesReport.value = salesRes.data
    renderChart()

    purchaseLog.value = logRes.data
      .sort((a, b) => new Date(b.time) - new Date(a.time)) // 時間新到舊
      .slice(0, 5) // 只取最新 5 筆
      .map(entry => ({
        ...entry,
        time: new Date(entry.time).toLocaleString()
      }))
  } catch (err) {
    console.error('載入報表失敗', err)
  }
})
</script>
