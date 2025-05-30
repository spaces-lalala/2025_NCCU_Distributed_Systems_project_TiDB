<template>
  <div class="p-6">
    <!-- Metabase Dashboard Embed -->
    <h2 class="text-xl font-bold mb-4">整體銷售分析 Dashboard</h2>
    <iframe
      v-if="metabaseEmbedUrl"
      :src="metabaseEmbedUrl"
      frameborder="0"
      width="300%"
      height="900"
      allowtransparency
      class="rounded-lg shadow mb-12"
    ></iframe>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const metabaseEmbedUrl = ref('')

onMounted(async () => {
  try {
    // 向你 Python FastAPI 後端請求嵌入用的 URL
    const res = await axios.get('http://localhost:8000/api/metabase_url') // 請根據實際 port 調整
    metabaseEmbedUrl.value = res.data.url
  } catch (err) {
    console.error('無法載入 Metabase 嵌入連結', err)
  }
})
</script>
