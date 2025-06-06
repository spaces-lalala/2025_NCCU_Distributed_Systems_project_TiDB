import http from 'k6/http';
import { check, group, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import { uuidv4 } from 'https://jslib.k6.io/k6-utils/1.4.0/index.js';

const BASE_URL = 'http://localhost:8000/api';

export let options = {
  stages: [
    { duration: '1m', target: 20 },
    { duration: '1m', target: 30 },
    { duration: '1m', target: 40 },
  ],
  thresholds: {
    http_req_duration: ['p(95)<500', 'p(99)<1000'],
    http_req_failed: ['rate<0.01'],
    checks: ['rate>0.99'],
    http_reqs: ['count>1000'],
    'http_req_duration{name:list_products}': ['p(95)<300'],
    'http_req_duration{name:create_order}': ['p(95)<700', 'p(99)<1500'],
    'http_req_duration{name:bestsellers_htap}': ['p(95)<1000'],
  },
};

const testUsers = new SharedArray('testUsers', function () {
  const users = [];
  for (let i = 0; i < options.stages[0].target * 2; i++) {
    users.push({
      name: `k6user_${uuidv4().substring(0, 8)}`,
      email: `k6user_${uuidv4().substring(0, 8)}@example.com`,
      password: 'k6Password123!',
    });
  }
  return users;
});

let productIds = [];

export default function () {
  const user = testUsers[__VU - 1];
  let authToken = '';

  group('01_User_Authentication', function () {
    if (__ITER === 0) {
      const registerPayload = {
        name: user.name,
        email: user.email,
        password: user.password,
      };
      const registerRes = http.post(`${BASE_URL}/auth/register`, JSON.stringify(registerPayload), {
        headers: { 'Content-Type': 'application/json' },
        tags: { name: 'register_user' },
      });

      if (registerRes.status === 201) {
        check(registerRes, {
          'Registration successful (201)': (r) => r.status === 201,
          'Response contains token': (r) => r.json() && r.json().token !== undefined,
        });
        authToken = registerRes.json().token;
        console.log(`VU ${__VU}: Registered and logged in as ${user.email}`);
      } else if (registerRes.status === 400 && registerRes.json()?.detail === "Email 已註冊") {
        console.log(`VU ${__VU}: User ${user.email} already registered, attempting login.`);
        const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
          email: user.email,
          password: user.password,
        }), {
          headers: { 'Content-Type': 'application/json' },
          tags: { name: 'login_user' },
        });

        check(loginRes, {
          'Login successful after existing (200)': (r) => r.status === 200,
          'Response contains token after existing': (r) => r.json()?.token !== undefined,
        });

        if (loginRes.status === 200) {
          authToken = loginRes.json().token;
          console.log(`VU ${__VU}: Logged in as existing user ${user.email}`);
        } else {
          console.error(`VU ${__VU}: Failed to log in existing user ${user.email}. Status: ${loginRes.status}, Body: ${loginRes.body}`);
        }
      } else {
        console.error(`VU ${__VU}: Registration failed for ${user.email}. Status: ${registerRes.status}, Body: ${registerRes.body}`);
      }
    } else {
      const loginRes = http.post(`${BASE_URL}/auth/login`, JSON.stringify({
        email: user.email,
        password: user.password,
      }), {
        headers: { 'Content-Type': 'application/json' },
        tags: { name: 'login_user' },
      });

      check(loginRes, {
        'Login successful (200)': (r) => r.status === 200,
        'Response contains token': (r) => r.json()?.token !== undefined,
      });

      if (loginRes.status === 200) {
        authToken = loginRes.json().token;
      } else {
        console.error(`VU ${__VU}: Failed to log in as ${user.email}. Status: ${loginRes.status}, Body: ${loginRes.body}`);
        return;
      }
    }
  });

  sleep(1);

  const authHeaders = {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${authToken}`,
  };

  group('02_Product_Browse_and_HTAP_Queries', function () {
    const productsRes = http.get(`${BASE_URL}/products?limit=20`, {
      headers: authHeaders,
      tags: { name: 'list_products' },
    });

    check(productsRes, {
      'Products list successful (200)': (r) => r.status === 200,
      'Products list is array': (r) => Array.isArray(r.json()),
    });

    if (productsRes.status === 200 && Array.isArray(productsRes.json())) {
      productIds = productsRes.json().map(p => p.id);
    } else {
      console.error(`VU ${__VU}: Failed to get product list. Status: ${productsRes.status}, Body: ${productsRes.body}`);
    }
    sleep(1);

    if (productIds.length > 0) {
      const randomProductId = productIds[Math.floor(Math.random() * productIds.length)];
      const productDetailRes = http.get(`${BASE_URL}/products/${randomProductId}`, {
        headers: authHeaders,
        tags: { name: 'get_product_details' },
      });

      check(productDetailRes, {
        'Product detail successful (200)': (r) => r.status === 200,
        'Product detail has name': (r) => r.json()?.name !== undefined,
      });
      sleep(1);
    }

    const bestsellersRes = http.get(`${BASE_URL}/products/bestsellers`, {
      headers: authHeaders,
      tags: { name: 'bestsellers_htap' },
    });
    check(bestsellersRes, {
      'Bestsellers successful (200)': (r) => r.status === 200,
      'Bestsellers is array': (r) => Array.isArray(r.json()),
    });
    sleep(1);

    const salesTrendsRes = http.get(`${BASE_URL}/analytics/sales-trends?days=30`, {
      headers: authHeaders,
      tags: { name: 'sales_trends_htap' },
    });
    check(salesTrendsRes, {
      'Sales trends successful (200)': (r) => r.status === 200,
      'Sales trends status success': (r) => r.json()?.status === 'success',
    });
    sleep(1);
  });

  group('03_Order_Creation_and_History', function () {
    if (productIds.length > 0) {
      const itemsToOrder = [];
      const numItems = Math.floor(Math.random() * 3) + 1;
      const chosenProductIds = [];

      for (let i = 0; i < numItems; i++) {
        let randomProductId;
        do {
          randomProductId = productIds[Math.floor(Math.random() * productIds.length)];
        } while (chosenProductIds.includes(randomProductId));
        chosenProductIds.push(randomProductId);

        itemsToOrder.push({
          product_id: randomProductId,
          quantity: Math.floor(Math.random() * 5) + 1,
        });
      }

      const orderPayload = {
        items: itemsToOrder,
        shipping_address: {
          address: "123 Main St",
          city: "Anytown",
          postal_code: "12345",
          country: "USA"
        },
        payment_method: "Credit Card"
      };

      const createOrderRes = http.post(`${BASE_URL}/orders`, JSON.stringify(orderPayload), {
        headers: authHeaders,
        tags: { name: 'create_order' },
      });

      check(createOrderRes, {
        'Order creation successful (201)': (r) => r.status === 201,
        'Order response has id': (r) => r.json()?.id !== undefined,
      });

      if (createOrderRes.status === 201) {
        const newOrderId = createOrderRes.json().id;
        console.log(`VU ${__VU}: Order created with ID: ${newOrderId}`);
        sleep(1);

        const simulatePaymentRes = http.post(`${BASE_URL}/payments/simulate/${newOrderId}`, null, {
          headers: authHeaders,
          tags: { name: 'simulate_payment' },
        });

        console.log(`Simulate payment response: ${simulatePaymentRes.status} - ${simulatePaymentRes.body}`);
    

        check(simulatePaymentRes, {
          'Payment simulation successful (200)': (r) => r.status === 200,
          'Payment status is PAID': (r) => r.json()?.status === 'PAID',
        });
       
      } else {
        console.error(`VU ${__VU}: Order creation failed. Status: ${createOrderRes.status}, Body: ${createOrderRes.body}`);
      }
    } else {
      console.warn(`VU ${__VU}: No product IDs available to create order. Ensure products are loaded.`);
    }

    const userOrdersRes = http.get(`${BASE_URL}/orders`, {
      headers: authHeaders,
      tags: { name: 'get_user_orders' },
    });
    check(userOrdersRes, {
      'User orders successful (200)': (r) => r.status === 200,
      'User orders is array': (r) => Array.isArray(r.json()),
    });
    sleep(1);

    const profileRes = http.get(`${BASE_URL}/auth/me`, {
      headers: authHeaders,
      tags: { name: 'get_user_profile' },
    });
    check(profileRes, {
      'Profile successful (200)': (r) => r.status === 200,
      'Profile has user data': (r) => r.json()?.id !== undefined,
    });
    sleep(1);
  });

  sleep(2);
}