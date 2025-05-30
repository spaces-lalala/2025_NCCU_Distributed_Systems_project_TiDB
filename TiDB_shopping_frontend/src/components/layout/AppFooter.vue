<template>
  <el-footer class="app-footer">
    <div class="footer-content">
      <div class="footer-main">
        <div class="footer-brand">
          <h4 class="brand-name">TiDB 購物網站</h4>
          <p class="brand-description">提供最優質的購物體驗</p>
        </div>
        
        <div class="footer-links">
          <div class="link-group">
            <h5 class="link-title">關於我們</h5>
            <ul class="link-list">
              <li><a href="/about">公司介紹</a></li>
              <li><a href="/careers">人才招募</a></li>
              <li><a href="/news">最新消息</a></li>
            </ul>
          </div>
          
          <div class="link-group">
            <h5 class="link-title">客戶服務</h5>
            <ul class="link-list">
              <li><a href="/contact">聯絡我們</a></li>
              <li><a href="/faq">常見問題</a></li>
              <li><a href="/shipping">配送資訊</a></li>
            </ul>
          </div>
          
          <div class="link-group">
            <h5 class="link-title">條款與政策</h5>
            <ul class="link-list">
              <li><a href="/terms">服務條款</a></li>
              <li><a href="/privacy">隱私權政策</a></li>
              <li><a href="/returns">退換貨政策</a></li>
            </ul>
          </div>
        </div>
      </div>
      
      <div class="footer-bottom">
        <div class="copyright">
          <p>&copy; {{ currentYear }} TiDB 購物網站. All Rights Reserved.</p>
        </div>
        <div class="tech-info">
          <p>Powered by TiDB - 混合事務和分析處理 (HTAP) 雲原生分散式資料庫</p>
        </div>
      </div>
    </div>
  </el-footer>
</template>

<script lang="ts" setup>
import { computed } from 'vue';

const currentYear = computed(() => new Date().getFullYear());
</script>

<style scoped>
.app-footer {
  background-color: var(--surface-color);
  border-top: 1px solid var(--border-color);
  margin-top: auto;
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.06);
}

.footer-content {
  max-width: var(--container-max-width);
  margin: 0 auto;
  padding: var(--spacing-xxl) var(--spacing-lg);
}

/* Footer Main Section */
.footer-main {
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: var(--spacing-xxl);
  margin-bottom: var(--spacing-xl);
  padding-bottom: var(--spacing-xl);
  border-bottom: 1px solid var(--border-light);
}

.footer-brand {
  max-width: 300px;
}

.brand-name {
  font-size: var(--font-size-lg);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-sm);
}

.brand-description {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: 0;
  line-height: 1.6;
}

/* Footer Links */
.footer-links {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--spacing-xl);
}

.link-group {
  margin: 0;
}

.link-title {
  font-size: var(--font-size-md);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--spacing-md);
}

.link-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.link-list li {
  margin-bottom: var(--spacing-sm);
}

.link-list a {
  color: var(--text-secondary);
  text-decoration: none;
  font-size: var(--font-size-sm);
  transition: var(--transition-base);
  display: inline-block;
  padding: 2px 0;
}

.link-list a:hover {
  color: var(--primary-color);
  transform: translateX(2px);
}

/* Footer Bottom */
.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--spacing-md);
}

.copyright p {
  font-size: var(--font-size-sm);
  color: var(--text-secondary);
  margin: 0;
}

.tech-info p {
  font-size: var(--font-size-xs);
  color: var(--text-tertiary);
  margin: 0;
  font-style: italic;
}

/* Responsive Design */
@media (max-width: 992px) {
  .footer-main {
    grid-template-columns: 1fr;
    gap: var(--spacing-xl);
  }
  
  .footer-links {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-lg);
  }
}

@media (max-width: 768px) {
  .footer-content {
    padding: var(--spacing-xl) var(--spacing-md);
  }
  
  .footer-main {
    gap: var(--spacing-lg);
    margin-bottom: var(--spacing-lg);
    padding-bottom: var(--spacing-lg);
  }
  
  .footer-links {
    grid-template-columns: 1fr;
    gap: var(--spacing-md);
  }
  
  .footer-bottom {
    flex-direction: column;
    text-align: center;
    gap: var(--spacing-sm);
  }
}

@media (max-width: 480px) {
  .footer-content {
    padding: var(--spacing-lg) var(--spacing-sm);
  }
  
  .brand-name {
    font-size: var(--font-size-md);
  }
  
  .brand-description {
    font-size: var(--font-size-xs);
  }
  
  .link-title {
    font-size: var(--font-size-sm);
  }
  
  .link-list a {
    font-size: var(--font-size-xs);
  }
}
</style>