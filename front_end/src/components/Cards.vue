<template>
  <div class="container">
    <!-- Header -->
    <header class="header">
      <nav class="nav">
        <a href="/home">Home</a>
        <a href="/cards">Cards</a>
        <a href="/investments">Investments</a>
      </nav>
      <div class="header-buttons">
        <button><img src="../assets/icons/messages.svg" alt="messages"/></button>
        <div class="account-menu-container">
          <button @click="toggleAccountMenu">
            <img src="../assets/icons/accout_icon.svg" alt="account"/>
          </button>
          <div v-if="showAccountMenu" class="account-menu">
            <button class="logout-button" @click="logoutUser">
              <img src="../assets/icons/logout.svg" alt="logout icon" class="logout-icon"/>
              Log Out
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Контейнер для позиціонування блоків -->
    <div class="layout-wrapper">
      <!-- Cards Title -->
      <h2 class="cards-title">Card</h2>

      <div class="container">
        <header>
        <span class="logo">
          <img src="../assets/logo.png" alt=""/>
          <h5>Master Card</h5>
        </span>
          <img src="../assets/chip.png" alt="" class="chip"/>
        </header>

        <div class="card-details">
          <div class="name-number">
            <h6>Card Number</h6>
            <h5 class="number">{{ cardNumber }}</h5>
            <h5 class="name">{{ cardHolder }}</h5>
          </div>
          <div class="valid-date">
            <h6>IBAN</h6>
            <h5>{{ cardIban }}</h5>
          </div>
        </div>
      </div>

      <!-- Subscriptions -->
      <div class="subscriptions-title">
        <img src="../assets/icons/subs.svg" alt="receipt icon"/>
        <h2>Subscriptions</h2>
      </div>

      <div class="subscriptions-box">
        <div
            class="subscription-item"
            v-for="(item, index) in subscriptions"
            :key="index"
        >
          <span class="dollar-icon">$</span>
          <span>{{ item.title }}</span>
          <span class="price">{{ item.payment_sum }}$</span>
        </div>

        <!-- Кнопка для відкриття форми -->
        <button class="add-subscription-button" @click="toggleForm">
          <span class="plus-icon">+</span>
        </button>

        <!-- Форма додавання -->
        <div v-if="showForm" class="add-subscription-form">
          <input type="text" v-model="newSubscription.title" placeholder="Назва підписки"/>
          <input type="text" v-model="newSubscription.description" placeholder="Опис"/>
          <input type="number" v-model="newSubscription.payment_sum" placeholder="Сума" step="0.01"/>
          <button @click="submitSubscription">Додати</button>
        </div>

        <hr/>
        <div class="total-cost">
          Total cost: <strong>{{ totalCost }}$</strong>
        </div>
      </div>

      <!-- Analytics Title -->
      <h2 class="analytics-title">Analytics</h2>

      <!-- Costs Card with Tabs -->
      <div class="costs-card">
        <div class="costs-header">
          <img
              :src="activeTab === 'costs' ? iconCosts : iconIncome"
              alt="icon"
              class="costs-icon"
          />
          <span class="costs-title">
      {{ activeTab === 'costs' ? 'Costs' : 'Income' }}
    </span>
        </div>

        <div class="costs-amount">
          {{ activeTab === 'costs' ? `${cardCosts}` + '₴' : `+${cardIncome}` + '₴' }}
        </div>

        <div class="arrow left" @click="switchTab">&#60;</div>
        <div class="arrow right" @click="switchTab">&#62;</div>

        <div class="meta-boxes">
          <div class="meta">
            <img src="../assets/icons/categories.svg" alt="categories"/>
            <div class="meta-number">
              {{ activeTab === 'costs' ? Object.keys(categoriesMap).length : Object.keys(categoriesMap).length }}
            </div>
            <div class="meta-label">Categories</div>
          </div>
          <div class="meta">
            <img src="../assets/icons/hashtag.svg" alt="tags"/>
            <div class="meta-number">0</div>
            <div class="meta-label">Tags</div>
          </div>
        </div>
      </div>

      <!-- Categories -->
      <div class="categories-box">
        <h3>Categories</h3>
        <div class="categories-list">
          <div v-if="Object.keys(categoriesMap).length">
            <div style="margin-bottom: 10px" v-for="(amount, category) in categoriesMap" :key="category">
              <span>{{ category }}: {{ amount }} грн</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Tags -->
      <div class="tags-box">
        <h3>Tags</h3>
        <div class="tags-list">
          <div>No tags</div>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <footer class="footer">
      <p>Email: <a href="mailto:moneytalks@gmail.com">moneytalks_need_5@gmail.com</a></p>
      <div class="social-icons">
        <i class="fab fa-instagram"></i>
        <i class="fab fa-linkedin"></i>
      </div>
    </footer>
  </div>
</template>

<script setup>
import {onMounted, ref, computed} from 'vue'
import iconCosts from '../assets/icons/costs.svg'
import iconIncome from '../assets/icons/income.svg'
import axios from 'axios'
import { useRouter } from 'vue-router';

const router = useRouter();

const showAccountMenu = ref(false)
const activeTab = ref('costs')
const cardNumber = ref('')
const cardHolder = ref('')
const cardIban = ref('')
const cardCosts = ref('')
const cardIncome = ref('')
const rawCategoriesMap = ref({})

function toggleAccountMenu() {
  showAccountMenu.value = !showAccountMenu.value
}

function switchTab() {
  activeTab.value = activeTab.value === 'costs' ? 'income' : 'costs'
}

const categoriesMap = computed(() => {
  const result = {}
  if (!rawCategoriesMap.value || typeof rawCategoriesMap.value !== 'object') return result

  for (const category in rawCategoriesMap.value) {
    const transactions = rawCategoriesMap.value[category]
    const total = transactions.reduce((sum, tx) => {
      const amount = tx.operationAmount
      return sum + (tx.hold ? 0 : amount)
    }, 0)

    if (activeTab.value === 'costs' && total < 0) {
      result[category] = (total / 100).toFixed(2)
    } else if (activeTab.value === 'income' && total > 0) {
      result[category] = (total / 100).toFixed(2)
    }
  }
  return result
})

onMounted(async () => {
  try {
    const token = localStorage.getItem("user-token")

    const response = await axios.get("http://0.0.0.0:8001/api/v1/monobank/token/", {
      headers: {Authorization: `JWT_TOKEN ${token}`},
    })

    const response2 = await axios.get("http://0.0.0.0:8001/api/v1/monobank/personal-info/", {
      headers: {Authorization: `JWT_TOKEN ${token}`},
    })

    const accounts = response2.data.accounts
    const accountWithMoney = accounts.find(acc => typeof acc.balance === 'number' && acc.balance > 0)

    if (accountWithMoney) {
      cardNumber.value = accountWithMoney.maskedPan?.[0] || '**** **** **** ****'
      cardHolder.value = response2.data.name || 'Unknown'
      cardIban.value = accountWithMoney.iban || '**** **** **** ****'

      const today = new Date()
      const tomorrow = new Date(today)
      tomorrow.setDate(today.getDate() + 1)
      const firstDay = new Date(today.getFullYear(), today.getMonth(), 1)

      const formatDate = (date) => {
        const dd = String(date.getDate()).padStart(2, '0')
        const mm = String(date.getMonth() + 1).padStart(2, '0')
        const yyyy = date.getFullYear()
        return `${dd}-${mm}-${yyyy}`
      }

      const dateFrom = formatDate(firstDay)
      const dateTo = formatDate(tomorrow)
      const accountId = accountWithMoney.id

      const statementResponse = await axios.get(
          `http://0.0.0.0:8001/api/v1/monobank/statement/${accountId}/${dateFrom}/${dateTo}/?category=true`,
          {
            headers: {
              Authorization: `JWT_TOKEN ${token}`,
            },
          }
      )

      const data = statementResponse.data
      rawCategoriesMap.value = data

      let totalPositive = 0
      let totalNegative = 0

      for (const key in data) {
        const transactions = data[key]

        transactions.forEach(transaction => {
          const amount = transaction.operationAmount
          if (!transaction.hold) {
            if (amount > 0) {
              totalPositive += amount
            } else {
              totalNegative += amount
            }
          }
        })
      }

      cardCosts.value = (totalNegative / 100).toFixed(2)
      cardIncome.value = (totalPositive / 100).toFixed(2)
    }

  } catch (error) {
    console.error('Помилка при завантаженні даних з monobank:', error)
  }

  await fetchSubscriptions()
})

/* ---------------------------- Підписки --------------------------------- */

const subscriptions = ref([])
const showForm = ref(false)
const newSubscription = ref({
  title: '',
  description: '',
  payment_sum: ''
})

const totalCost = computed(() =>
    subscriptions.value.reduce((sum, sub) => sum + parseFloat(sub.payment_sum), 0).toFixed(2)
)

function toggleForm() {
  showForm.value = !showForm.value
}

async function fetchSubscriptions() {
  try {
    const token = localStorage.getItem("user-token")
    console.log('token')
    console.log(token)
    const userResponse = await axios.get(
        "http://0.0.0.0:8001/api/v1/me",
        {
          headers: {
            Authorization: `JWT_TOKEN ${token}`,
          },
        }
    )

    const userId = userResponse.data.id
    console.log(userId)
    const response = await axios.get(`http://0.0.0.0:8001/api/v1/subscriptions/?user=${userId}`, {
      headers: {
        Authorization: `JWT_TOKEN ${token}`,
      },
    })
    subscriptions.value = response.data
    console.log('response.data')
    console.log(response.data)
  } catch (error) {
    console.error('Помилка при завантаженні підписок:', error)
  }
}

async function submitSubscription() {
  const token = localStorage.getItem("user-token")

  try {
    const response = await axios.post(
        "http://0.0.0.0:8001/api/v1/subscriptions/",
        {
          title: newSubscription.value.title,
          description: newSubscription.value.description,
          payment_sum: newSubscription.value.payment_sum
        },
        {
          headers: {
            Authorization: `JWT_TOKEN ${token}`
          }
        }
    )

    subscriptions.value.push(response.data)
    newSubscription.value = {
      title: '',
      description: '',
      payment_sum: ''
    }
    showForm.value = false
  } catch (error) {
    console.error('Помилка при додаванні підписки:', error)
  }
}

async function logoutUser() {
  const refresh = localStorage.getItem('user-refresh');
  try {
    await axios.post('http://0.0.0.0:8000/api/logout/', { refresh }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('user-token')}`
      }
    });
  } catch (err) {
    console.error('Logout error:', err);
  }

  localStorage.removeItem('user-token');
  localStorage.removeItem('user-refresh');

  router.push('/login');
}
</script>


<style scoped>
.layout-wrapper {
  position: relative;
  width: 100%;
  min-height: 1500px;
}

/* Cards Title */
.cards-title {
  position: absolute;
  top: 25px;
  left: 258px;
  width: 254px;
  height: 54px;
  font-size: 28px;
  font-weight: bold;
}

@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap");

/* Card-specific styles */
.layout-wrapper .container {
  position: absolute;
  top: 100px;
  left: 67px;
  background-image: url("../assets/bg.png");
  background-size: cover;
  padding: 25px;
  border-radius: 28px;
  max-width: 437px;
  width: 100%;
  height: 252px;
  box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
  background-color: #2b2b2b;
}

.layout-wrapper .container header,
.layout-wrapper .container .logo {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.layout-wrapper .container .logo img {
  width: 48px;
  margin-right: 10px;
}

.layout-wrapper .container h5 {
  font-size: 16px;
  font-weight: 400;
  color: #fff;
}

.layout-wrapper .container header .chip {
  width: 60px;
}

.layout-wrapper .container h6 {
  color: #fff;
  font-size: 10px;
  font-weight: 400;
}

.layout-wrapper .container h5.number {
  margin-top: 4px;
  font-size: 18px;
  letter-spacing: 1px;
}

.layout-wrapper .container h5.name {
  margin-top: 20px;
}

.layout-wrapper .container .card-details {
  margin-top: 40px;
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}


/* Subscriptions Title */
.subscriptions-title {
  position: absolute;
  top: 20px;
  left: 1125px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 26px;
}

.subscriptions-box {
  position: absolute;
  top: 120px;
  left: 950px;
  width: 620px;
  height: 400px;
  border-radius: 40px;
  background-color: #2D6A4F3B;
  padding: 1.5rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.add-subscription-button {
  background-color: transparent;
  border: none;
  cursor: pointer;
  padding: 4px;
  display: flex;
  margin-left: 298px;
  align-items: center;
  justify-content: center;
}

.plus-icon {
  font-size: 24px;
  font-weight: bold;
  color: #4CAF50;
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  border-radius: 50%;
  background-color: #e0f7e9;
}

.add-subscription-form {
  background-color: #6fae6e;
  padding: 8px 12px;
  border-radius: 6px;
  display: flex;
  gap: 8px;
  align-items: center;
  box-shadow: 0 2px 5px rgb(0 0 0 / 0.15);
  width: 100%; /* по ширині контейнера */
  box-sizing: border-box;
}

.add-subscription-form input {
  padding: 6px 10px;
  border: none;
  border-radius: 4px;
  font-size: 14px;
  color: #1b4332;
  background-color: #dcedc8;
  outline: none;
  flex-grow: 1; /* інпути розтягуються пропорційно */
  min-width: 0; /* щоб flex-grow працював коректно */
  transition: background-color 0.2s ease;
}

.add-subscription-form input::placeholder {
  color: #4caf50;
}

.add-subscription-form input:focus {
  background-color: #c5e1a5;
}

.add-subscription-form button {
  padding: 6px 14px;
  background-color: #4caf50;
  color: white;
  font-weight: 600;
  font-size: 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.25s ease;
  flex-shrink: 0; /* кнопка не стискається */
  margin-left: 8px;
  white-space: nowrap; /* щоб текст не переносився */
}


.subscription-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-radius: 18px;
  margin-bottom: 12px;
  font-size: 1.5rem;
  font-weight: 700;
}

.subscription-item .dollar-icon,
.subscription-item .price {
  font-weight: 700;
  font-size: 1.5rem;
}

.total-cost {
  margin-top: 10px;
  text-align: right;
}

/* Analytics Title */
.analytics-title {
  position: absolute;
  top: 760px;
  left: 50%;
  transform: translateX(-50%);
  font-size: 28px;
}

/* Costs Card */

.costs-card {
  position: absolute;
  top: 900px;
  left: 70px;
  width: 478px;
  height: 420px;
  border-radius: 42px;
  background-color: #d0e0d8;
  padding: 2rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  font-family: 'Poppins', sans-serif;
}

.costs-header {
  position: relative;
  width: 100%;
  height: 64px;
  margin-bottom: 1rem;
}

.costs-icon {
  position: absolute;
  left: 0;
  top: 50%;
  transform: translateY(-50%);
  width: 48px;
  height: 48px;
}

.costs-title {
  font-size: 40px;
  font-weight: 700;
  color: #0b2e20;
  text-align: center;
  display: block;
  width: 100%;
  position: absolute;
  top: 50%;
  left: 0;
  transform: translateY(-50%);
}

.costs-amount {
  font-size: 32px;
  font-weight: 800;
  color: #072b16;
  text-align: center;
  margin-top: 50px;
  margin-bottom: 40px;
}

.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  font-size: 24px;
  font-weight: bold;
  color: #a5d6a7;
  cursor: pointer;
}

.arrow.left {
  left: 18px;
}

.arrow.right {
  right: 18px;
}

.meta-boxes {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 40px;
  margin-top: 1rem;
  gap: 1rem;
  width: 100%;
}

.meta {
  width: 226px;
  height: 185px;
  background-color: #6fae6e;
  color: #eaf6eb;
  border-radius: 30px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.meta img {
  width: 24px;
  height: 24px;
  margin-bottom: 0.5rem;
}

.meta-number {
  font-size: 24px;
  font-weight: bold;
}

.meta-label {
  font-size: 14px;
  font-weight: 600;
  margin-top: 4px;
}

/* Categories */
.categories-box {
  position: absolute;
  top: 900px;
  left: 1025px;
  width: 510px;
  height: 208px;
  border-radius: 50px;
  background: #CEDCD6;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;
}

.categories-box h3 {
  margin: 0;
  font-size: 28px;
  color: #7AAD85;
  padding-top: 15px;
  padding-left: 10px;
}

.categories-list {
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  gap: 12px;
  padding-bottom: 8px;
}

.categories-list > div {
  flex: 0 0 auto;
  white-space: nowrap;
  padding: 8px 14px;
  border-radius: 16px;
  font-weight: bold;
  font-size: 20px;
}

.categoria {
  display: flex;
  justify-content: space-between;
  align-content: center;
}

/* Tags */
.tags-box {
  position: absolute;
  top: 1180px;
  left: 1025px;
  width: 510px;
  height: 208px;
  border-radius: 50px;
  background: #CEDCD6;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  overflow: hidden;
}

.tags-box h3 {
  margin: 0;
  font-size: 28px;
  color: #7AAD85;
  padding-top: 15px;
  padding-left: 10px;
}

.tags-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  overflow-y: auto;
}

.tags-list > div {
  padding: 8px 14px;
  border-radius: 16px;
  font-weight: bold;
  font-size: 20px;
}

.categories-list,
.tags-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  overflow-y: auto;
  padding-right: 6px;
  max-height: 140px;
}

/* Уніфікований стиль скроллбару */
.categories-list::-webkit-scrollbar,
.tags-list::-webkit-scrollbar {
  width: 6px;
}

.categories-list::-webkit-scrollbar-thumb,
.tags-list::-webkit-scrollbar-thumb {
  background: #6fae6e;
  border-radius: 3px;
}

.categories-list::-webkit-scrollbar-track,
.tags-list::-webkit-scrollbar-track {
  background: transparent;
}


</style>
