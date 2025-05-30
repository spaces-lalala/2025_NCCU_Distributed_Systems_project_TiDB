#!/usr/bin/env node

// UI 功能自動化測試腳本
// 用於檢查前端應用的基本功能是否正常

const puppeteer = require('puppeteer');
const fs = require('fs');

const BASE_URL = 'http://localhost:5002';
const TIMEOUT = 10000;

class UITester {
    constructor() {
        this.browser = null;
        this.page = null;
        this.results = {
            passed: 0,
            failed: 0,
            tests: []
        };
    }

    async init() {
        console.log('🚀 啟動 UI 功能測試...');
        this.browser = await puppeteer.launch({ 
            headless: false, // 顯示瀏覽器，方便觀察
            defaultViewport: { width: 1200, height: 800 }
        });
        this.page = await this.browser.newPage();
        
        // 設置控制台日誌監聽
        this.page.on('console', msg => {
            if (msg.type() === 'error') {
                console.log('❌ Console Error:', msg.text());
            }
        });
        
        // 設置錯誤監聽
        this.page.on('pageerror', error => {
            console.log('❌ Page Error:', error.message);
        });
    }

    async test(name, testFn) {
        try {
            console.log(`\n📋 測試: ${name}`);
            await testFn();
            console.log(`✅ 通過: ${name}`);
            this.results.passed++;
            this.results.tests.push({ name, status: 'PASS' });
        } catch (error) {
            console.log(`❌ 失敗: ${name} - ${error.message}`);
            this.results.failed++;
            this.results.tests.push({ name, status: 'FAIL', error: error.message });
        }
    }

    async testHomePage() {
        await this.test('首頁載入', async () => {
            await this.page.goto(BASE_URL, { waitUntil: 'networkidle0' });
            await this.page.waitForSelector('.home-page', { timeout: TIMEOUT });
            
            const title = await this.page.title();
            if (!title.includes('購物網站')) {
                throw new Error('頁面標題不正確');
            }
        });
    }

    async testProductList() {
        await this.test('商品列表頁載入', async () => {
            await this.page.goto(`${BASE_URL}/products`, { waitUntil: 'networkidle0' });
            await this.page.waitForSelector('.product-list-page', { timeout: TIMEOUT });
            
            // 檢查是否有商品卡片
            const productCards = await this.page.$$('.product-card');
            if (productCards.length === 0) {
                throw new Error('沒有找到商品卡片');
            }
        });
    }

    async testProductDetail() {
        await this.test('商品詳情頁載入', async () => {
            await this.page.goto(`${BASE_URL}/product/1`, { waitUntil: 'networkidle0' });
            await this.page.waitForSelector('.product-detail-page', { timeout: TIMEOUT });
            
            // 檢查商品資訊是否顯示
            const productTitle = await this.page.$('.product-title');
            if (!productTitle) {
                throw new Error('商品標題未顯示');
            }
            
            // 檢查數量選擇器
            const quantityInput = await this.page.$('.quantity-input input');
            if (!quantityInput) {
                throw new Error('數量選擇器未找到');
            }
            
            // 檢查加入購物車按鈕
            const addButton = await this.page.$('.add-to-cart-button');
            if (!addButton) {
                throw new Error('加入購物車按鈕未找到');
            }
        });
    }

    async testAddToCart() {
        await this.test('加入購物車功能', async () => {
            await this.page.goto(`${BASE_URL}/product/1`, { waitUntil: 'networkidle0' });
            await this.page.waitForSelector('.add-to-cart-button', { timeout: TIMEOUT });
            
            // 檢查購物車數量初始值
            const initialCartCount = await this.page.$eval('.cart-badge', el => el.textContent || '0');
            
            // 點擊加入購物車
            await this.page.click('.add-to-cart-button');
            
            // 等待成功消息
            await this.page.waitForSelector('.el-message--success', { timeout: 5000 });
            
            // 檢查購物車數量是否增加
            await this.page.waitForFunction(
                (initial) => {
                    const badge = document.querySelector('.cart-badge');
                    return badge && parseInt(badge.textContent || '0') > parseInt(initial);
                },
                {},
                initialCartCount
            );
        });
    }

    async testCartPage() {
        await this.test('購物車頁面', async () => {
            await this.page.goto(`${BASE_URL}/cart`, { waitUntil: 'networkidle0' });
            await this.page.waitForSelector('.cart-page', { timeout: TIMEOUT });
            
            // 檢查是否有購物車內容或空購物車提示
            const hasItems = await this.page.$('.cart-item');
            const emptyCart = await this.page.$('.empty-cart-section');
            
            if (!hasItems && !emptyCart) {
                throw new Error('購物車頁面內容異常');
            }
        });
    }

    async testBestSellers() {
        await this.test('熱銷排行榜頁面', async () => {
            await this.page.goto(`${BASE_URL}/bestsellers`, { waitUntil: 'networkidle0' });
            await this.page.waitForSelector('.best-sellers-page', { timeout: TIMEOUT });
            
            // 檢查 HTAP 展示區域
            const htapShowcase = await this.page.$('.htap-showcase');
            if (!htapShowcase) {
                throw new Error('HTAP 展示區域未找到');
            }
        });
    }

    async testResponsiveDesign() {
        await this.test('響應式設計 - 手機版', async () => {
            await this.page.setViewport({ width: 375, height: 667 });
            await this.page.goto(BASE_URL, { waitUntil: 'networkidle0' });
            await this.page.waitForSelector('.home-page', { timeout: TIMEOUT });
            
            // 檢查導航是否適應手機版
            const navbar = await this.page.$('.app-navbar');
            if (!navbar) {
                throw new Error('導航欄在手機版下未正確顯示');
            }
        });

        await this.test('響應式設計 - 桌面版', async () => {
            await this.page.setViewport({ width: 1200, height: 800 });
            await this.page.goto(BASE_URL, { waitUntil: 'networkidle0' });
            await this.page.waitForSelector('.home-page', { timeout: TIMEOUT });
        });
    }

    async testErrorHandling() {
        await this.test('錯誤處理 - 不存在的商品', async () => {
            await this.page.goto(`${BASE_URL}/product/999`, { waitUntil: 'networkidle0' });
            await this.page.waitForSelector('.not-found-section', { timeout: TIMEOUT });
            
            const notFoundMessage = await this.page.$('.not-found-title');
            if (!notFoundMessage) {
                throw new Error('商品未找到頁面未正確顯示');
            }
        });
    }

    async runAllTests() {
        try {
            await this.init();
            
            console.log('🎯 開始執行完整 UI 功能測試\n');
            
            await this.testHomePage();
            await this.testProductList();
            await this.testProductDetail();
            await this.testAddToCart();
            await this.testCartPage();
            await this.testBestSellers();
            await this.testResponsiveDesign();
            await this.testErrorHandling();
            
            this.generateReport();
            
        } catch (error) {
            console.error('測試執行失敗:', error);
        } finally {
            if (this.browser) {
                await this.browser.close();
            }
        }
    }

    generateReport() {
        console.log('\n📊 測試結果報告');
        console.log('=' * 50);
        console.log(`✅ 通過: ${this.results.passed}`);
        console.log(`❌ 失敗: ${this.results.failed}`);
        console.log(`📈 成功率: ${((this.results.passed / (this.results.passed + this.results.failed)) * 100).toFixed(1)}%`);
        
        console.log('\n📋 詳細結果:');
        this.results.tests.forEach(test => {
            const status = test.status === 'PASS' ? '✅' : '❌';
            console.log(`${status} ${test.name}${test.error ? ` - ${test.error}` : ''}`);
        });

        // 保存報告到文件
        const report = {
            timestamp: new Date().toISOString(),
            summary: {
                passed: this.results.passed,
                failed: this.results.failed,
                total: this.results.passed + this.results.failed,
                successRate: ((this.results.passed / (this.results.passed + this.results.failed)) * 100).toFixed(1)
            },
            tests: this.results.tests
        };

        fs.writeFileSync('ui-test-report.json', JSON.stringify(report, null, 2));
        console.log('\n📄 詳細報告已保存到 ui-test-report.json');
    }
}

// 執行測試
if (require.main === module) {
    const tester = new UITester();
    tester.runAllTests().catch(console.error);
}

module.exports = UITester;
