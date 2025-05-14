import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';

// Import page components using dynamic imports for route-level code splitting
const HomePage = () => import('@/views/HomePage.vue');
const ProductListPage = () => import('@/views/ProductListPage.vue');
const ProductDetailPage = () => import('@/views/ProductDetailPage.vue');
const CartPage = () => import('@/views/CartPage.vue');
const LoginPage = () => import('@/views/LoginPage.vue'); // Assuming LoginPage.vue will be created
const RegisterPage = () => import('@/views/RegisterPage.vue');
const MemberProfilePage = () => import('@/views/MemberProfilePage.vue'); // Assuming MemberProfilePage.vue will be created
const BestSellersPage = () => import('@/views/BestSellersPage.vue'); // Assuming BestSellersPage.vue will be created
const CheckoutPage = () => import('@/views/CheckoutPage.vue'); // Assuming CheckoutPage.vue will be created
const OrderConfirmationPage = () => import('@/views/OrderConfirmationPage.vue'); // Assuming OrderConfirmationPage.vue will be created
const NotFoundPage = () => import('@/views/NotFoundPage.vue'); // Assuming NotFoundPage.vue will be created

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
    meta: { title: '首頁' },
  },
  {
    path: '/products',
    name: 'ProductList',
    component: ProductListPage,
    meta: { title: '商品列表' },
  },
  {
    path: '/product/:id', // Dynamic segment for product ID
    name: 'ProductDetail',
    component: ProductDetailPage,
    props: true, // Pass route params as component props
    meta: { title: '商品詳情' },
  },
  {
    path: '/cart',
    name: 'Cart',
    component: CartPage,
    meta: { title: '購物車' },
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginPage,
    meta: { title: '登入' },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterPage, // This should now correctly point to your RegisterPage.vue
    meta: { title: '註冊' },
  },
  {
    path: '/profile',
    name: 'MemberProfile',
    component: MemberProfilePage,
    meta: { requiresAuth: true, title: '會員中心' }, // Example: Mark routes that require authentication
  },
  {
    path: '/bestsellers',
    name: 'BestSellers',
    component: BestSellersPage,
    meta: { title: '熱銷排行榜' },
  },
  {
    path: '/checkout',
    name: 'Checkout',
    component: CheckoutPage,
    meta: { requiresAuth: true, title: '結帳' },
  },
  {
    path: '/order-confirmation',
    name: 'OrderConfirmation',
    component: OrderConfirmationPage,
    meta: { requiresAuth: true, title: '訂單完成' },
  },
  // Catch-all 404 route - must be the last route
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundPage,
    meta: { title: '頁面未找到' },
  },
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition;
    } else {
      return { top: 0 };
    }
  },
});

// Simple navigation guard (example)
// You should refine this based on your actual authentication state management (e.g., Pinia store)
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('authToken'); // Placeholder for auth check

  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } });
  } else if ((to.name === 'Login' || to.name === 'Register') && isAuthenticated && to.name !== 'Home') {
    // If user is authenticated and tries to access login/register, redirect to home
    // Avoid redirecting if already going to Home from login/register to prevent loop if home requires auth
    // Or redirect to a specific dashboard/profile page
    next({ name: 'Home' });
  }
  else {
    next();
  }
});

// Update document title after navigation
router.afterEach((to) => {
  document.title = to.meta.title ? `${to.meta.title} - 購物網站` : '購物網站';
});

export default router; 