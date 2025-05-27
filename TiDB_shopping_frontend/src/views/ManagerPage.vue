<template>
  <div class="p-6">
    <h2 class="text-xl font-bold mb-4">產品銷售排行榜</h2>

    <!-- 表格 -->
    <el-table :data="salesReport" stripe class="mb-8">
      <el-table-column prop="product_name" label="產品名稱" />
      <el-table-column prop="total_sold" label="總銷售數量" />
    </el-table>

    <!-- 圓餅圖容器 -->
    <div ref="chartRef" style="width: 100%; height: 400px;" />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

const salesReport = ref([])
const chartRef = ref(null)
let chartInstance = null

// 初始化圖表
const renderChart = () => {
  if (!chartRef.value) return

  const total = salesReport.value.reduce((sum, item) => sum + item.total_sold, 0)

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
    const res = await axios.get('/api/admin/sales_report', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('token')}`
      }
    })
    salesReport.value = res.data
  } catch (err) {
    console.error('無法載入報表', err)
  }
})

// 當資料更新後重新渲染圖表
watch(salesReport, () => {
  renderChart()
})
</script>
