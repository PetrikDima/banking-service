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
          <Item
            name="Bitcoin"
            trading_key="BTC"
            :img="bitcoinIcon"
            @select="handleCryptoSelect"
            :isSelected="selectedCrypto === 'BTC'"
          />
          <Item
            name="Ethereum"
            trading_key="ETH"
            :img="ethereumIcon"
            @select="handleCryptoSelect"
            :isSelected="selectedCrypto === 'ETH'"
          />
          <Item
            name="BNB"
            trading_key="BNB"
            :img="bnbIcon"
            @select="handleCryptoSelect"
            :isSelected="selectedCrypto === 'BNB'"
          />
          <Item
            name="Solana"
            trading_key="SOL"
            :img="solanaIcon"
            @select="handleCryptoSelect"
            :isSelected="selectedCrypto === 'SOL'"
          />
          <Item
            name="XRP"
            trading_key="XRP"
            :img="xrpIcon"
            @select="handleCryptoSelect"
            :isSelected="selectedCrypto === 'XRP'"
          />
        </div>

        <div v-if="selectedCrypto">
          <h2 style="text-align: center">Analysis</h2>
          <div class="chart-section">
            <div v-if="isLoading" class="spinner-overlay">
              <div class="spinner-wrapper">
                <div class="spinner"></div>
                <p class="spinner-text">
                  Loading data<span class="dots"><span>.</span><span>.</span><span>.</span></span>
                </p>
              </div>
            </div>

            <div class="chart-and-markets" :style="{ opacity: isLoading ? 0.3 : 1, pointerEvents: isLoading ? 'none' : 'auto' }">
              <div class="chart-container">
                <LineChart :data="crypto_prices" :label="selectedCrypto" />
                <div class="chart-description">
                  <p>
                    Solana has shown a steady recovery throughout May 2025, with notable growth around the middle of the month.
                    Despite some short-term pullbacks, the trend remains optimistic due to increased developer activity and growing DeFi adoption on the network.
                  </p>
                </div>
              </div>

              <div class="market-prices">
                <h3>Trading</h3>
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
import { investments } from "@/scripts/investments.js"

const exchangePrices = ref({})
const selectedCrypto = ref('')
const crypto_prices = ref([])
const isLoading = ref(false)

const showAccountMenu = ref(false)

function toggleAccountMenu() {
  showAccountMenu.value = !showAccountMenu.value
}

function logoutUser() {
  console.log('Logging out...')
}

async function handleCryptoSelect(symbol) {
  if (selectedCrypto.value === symbol) {
    selectedCrypto.value = ''
    return
  }

  isLoading.value = true
  selectedCrypto.value = symbol

  try {
    const result = await investments.getTradingByName(symbol)
    exchangePrices.value = result || {}

    const result1 = await investments.getPriceByName(symbol)
    crypto_prices.value = Array.isArray(result1) ? result1 : []
  } catch (error) {
    console.error('Error loading crypto data:', error)
  } finally {
    isLoading.value = false
  }
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
  position: relative;
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
  background-color: #ffffff;
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
  font-size: 0.95rem;
  z-index: 1;
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

/* Spinner styles */
.spinner-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
}

.spinner-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.spinner {
  border: 4px solid #d1fae5;
  border-top: 4px solid #065f46;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 0.8s linear infinite;
}

.spinner-text {
  font-size: 1rem;
  color: #065f46;
  font-weight: 500;
  text-align: center;
}

.dots span {
  opacity: 0;
  animation: dotsAnimation 1.5s infinite;
  display: inline-block;
}

.dots span:nth-child(1) {
  animation-delay: 0s;
}
.dots span:nth-child(2) {
  animation-delay: 0.2s;
}
.dots span:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes dotsAnimation {
  0% {
    opacity: 0;
  }
  30% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>
