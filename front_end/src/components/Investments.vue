<template>
  <div class="page-wrapper">
    <header class="header">
      <nav class="nav">
        <a href="#">Home</a>
        <a href="/cards">Cards</a>
        <a href="/investments">Investments</a>
      </nav>
      <div class="header-buttons">
        <button><img src="../assets/icons/messages.svg" alt="messages" /></button>
        <div class="account-menu-container">
          <button @click="toggleAccountMenu">
            <img src="../assets/icons/accout_icon.svg" alt="account" />
          </button>
          <div v-if="showAccountMenu" class="account-menu">
            <button class="logout-button" @click="logoutUser">
              <img src="../assets/icons/logout.svg" alt="logout icon" class="logout-icon" />
              Log Out
            </button>
          </div>
        </div>
      </div>
    </header>

    <main class="content">
      <section>
        <h2 style="text-align: center">Cryptocurrency</h2>
        <div class="grid">
          <Item name="Bitcoin" :img="bitcoinIcon" />
          <Item name="Ethereum" :img="ethereumIcon" />
          <Item name="BNB" :img="bnbIcon" />
          <Item name="Solana" :img="solanaIcon" />
          <Item name="XRP" :img="xrpIcon" />
        </div>

        <h2 style="text-align: center">Analysis</h2>
        <div class="chart-section">
          <h2>Solana (SOL) Price Chart</h2>

          <div class="chart-and-markets">
            <div class="chart-container">
              <LineChart :data="solanaPrices" label="SOL" />
              <div class="chart-description">
                <p>
                  Solana has shown a steady recovery throughout May 2025, with notable growth around the middle of the month.
                  Despite some short-term pullbacks, the trend remains optimistic due to increased developer activity and growing DeFi adoption on the network.
                </p>
              </div>
            </div>

            <div class="market-prices">
              <h3>Exchange Prices</h3>
              <ul>
                <li v-for="(exchange, name) in exchangePrices" :key="name">
                  <span class="exchange-name">{{ name }}</span>
                  <span class="exchange-price">${{ exchange.price.toFixed(2) }}</span>
                  <a :href="exchange.trade_link" target="_blank" class="trade-button">Trade</a>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <p>Email: <a href="mailto:moneytalks_need_5@gmail.com">moneytalks_need_5@gmail.com</a></p>
      <div class="social-icons">
        <i class="fab fa-instagram"></i>
        <i class="fab fa-linkedin"></i>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Item from './InvestmentsItem.vue'
import LineChart from './LineChart.vue'

import bitcoinIcon from '../assets/icons/bitcoin_icon.svg'
import ethereumIcon from '../assets/icons/ethereum_icon.svg'
import bnbIcon from '../assets/icons/bnb_icon.svg'
import solanaIcon from '../assets/icons/solana_icon.svg'
import xrpIcon from '../assets/icons/xrp_icon.svg'

const showAccountMenu = ref(false)

function toggleAccountMenu() {
  showAccountMenu.value = !showAccountMenu.value
}

function logoutUser() {
  console.log('Logging out...')
}

const solanaPrices = [
  { date: '2025-05-02', price: 150.76 },
  { date: '2025-05-03', price: 147.97 },
  { date: '2025-05-04', price: 146.8 },
  { date: '2025-05-05', price: 143.98 },
  { date: '2025-05-06', price: 146.81 },
  { date: '2025-05-07', price: 146.91 },
  { date: '2025-05-08', price: 147.2 },
  { date: '2025-05-09', price: 163.42 },
  { date: '2025-05-10', price: 172.7 },
  { date: '2025-05-11', price: 177.34 },
  { date: '2025-05-12', price: 172.86 },
  { date: '2025-05-13', price: 174.42 },
  { date: '2025-05-14', price: 184.05 },
  { date: '2025-05-15', price: 176.46 },
  { date: '2025-05-16', price: 168.75 },
  { date: '2025-05-17', price: 167.77 },
  { date: '2025-05-18', price: 165.94 },
  { date: '2025-05-19', price: 171.54 },
  { date: '2025-05-20', price: 166.71 },
  { date: '2025-05-21', price: 168.39 },
  { date: '2025-05-22', price: 173.97 },
  { date: '2025-05-23', price: 179.58 },
  { date: '2025-05-24', price: 174.44 },
  { date: '2025-05-25', price: 176.0 },
  { date: '2025-05-26', price: 175.13 },
  { date: '2025-05-27', price: 174.72 },
  { date: '2025-05-28', price: 176.58 },
  { date: '2025-05-29', price: 172.12 },
  { date: '2025-05-30', price: 166.84 },
  { date: '2025-05-31', price: 155.2 },
]

const exchangePrices = {
  Binance: {
    price: 154.58,
    trade_link: 'https://www.binance.com/en/trade/SOLUSDT',
  },
  Bitget: {
    price: 154.56,
    trade_link: 'https://www.bitget.com/en/spot/SOLUSDT',
  },
  Bybit: {
    price: 154.59,
    trade_link: 'https://www.bybit.com/en/trade/spot/SOLUSDT',
  },
  KuCoin: {
    price: 154.604,
    trade_link: 'https://www.kucoin.com/trade/SOL-USDT',
  },
  OKX: {
    price: 154.58,
    trade_link: 'https://www.okx.com/trade-spot/SOL-USDT',
  },
}
</script>

<style scoped>
.page-wrapper {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.content {
  flex: 1;
}

.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px 60px;
  max-width: 800px;
  margin: 50px auto;
  justify-items: center;
  align-items: center;
}

.grid > .item:nth-child(4) {
  grid-column: 1 / 2;
}

.grid > .item:nth-child(5) {
  grid-column: 3 / 4;
}

.footer {
  height: 60px;
  background: linear-gradient(to top, #1A7431CC 0%, #1A743100 100%);
  color: white;
  padding: 1rem 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer p a {
  color: #dbfeb8;
  text-decoration: none;
  transition: color 0.2s;
}

.footer p a:hover {
  color: #d1fae5;
}

.social-icons {
  display: flex;
  gap: 1rem;
  font-size: 1.25rem;
}

.chart-section {
  max-width: 1200px;
  margin: 3rem auto;
  padding: 1rem;
  text-align: center;
}

.chart-and-markets {
  display: flex;
  gap: 2rem;
  align-items: flex-start;
  justify-content: center;
  flex-wrap: wrap;
}

.chart-container {
  flex: 1 1 600px;
  z-index: 1;
}

.chart-description {
  background-color: #f3f4f6;
  padding: 1.5rem;
  border-radius: 12px;
  text-align: left;
  font-size: 1rem;
  line-height: 1.6;
  color: #111827;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  margin-top: 2rem;
}

.market-prices {
  flex: 0 0 220px;
  background-color: #ffffff; /* ← повністю непрозорий білий */
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  font-size: 0.95rem;
  z-index: 1; /* на всяк випадок */
}

.market-prices h3 {
  margin-bottom: 1rem;
  font-size: 1.15rem;
  color: #065f46;
  text-align: center;
}

.market-prices ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.market-prices li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  gap: 0.5rem;
}

.exchange-name {
  font-weight: 600;
  flex: 1;
}

.exchange-price {
  color: #065f46;
}

.trade-button {
  background-color: #065f46;
  color: white;
  padding: 0.25rem 0.6rem;
  border-radius: 4px;
  text-decoration: none;
  font-size: 0.85rem;
  transition: background-color 0.2s;
}

.trade-button:hover {
  background-color: #047857;
}
</style>
