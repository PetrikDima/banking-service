<template>
  <div class="container">
    <!-- Top Nav -->
    <img src="../assets/money_talks_background.jpg" alt="background" class="background-image">
    <header class="header">
      <nav class="nav">
        <a href="#">Home</a>
        <a href="/cards">Cards</a>
        <a href="/investments">Investments</a>
      </nav>
      <div class="header-buttons">
        <button><img src="../assets/icons/messages.svg" alt="messages"></button>
        <div class="account-menu-container">
          <button @click="toggleAccountMenu">
            <img src="../assets/icons/accout_icon.svg" alt="account"/>
          </button>

          <div v-if="showAccountMenu" class="account-menu">
            <button class="logout-button">
              <img src="../assets/icons/logout.svg" alt="logout icon" class="logout-icon"/>
              Log Out
            </button>
          </div>
        </div>
      </div>
    </header>

    <!-- Info Section -->
    <section class="info-section">
      <div class="info-about-company">
        <div class="info-text-block">
          <h1>Info about project</h1>
          <p>
            This personal finance planning service is a side project by two friends aiming to help users better manage
            their money. It allows tracking income and expenses, setting financial goals, and analyzing spending habits
            through clear visualizations. Built with Django (DRF), Vue.js, and PostgreSQL, it also supports banking API
            integrations like Monobank for automatic transaction syncing.
          </p>
          <a href="https://github.com/PetrikDima/banking-service" target="_blank" rel="noopener noreferrer">
            <button class="btn-primary">Read more &gt;</button>
          </a>
        </div>
      </div>
    </section>

    <!-- News Section -->
    <section class="news-section">
      <h2 style="font-size: 40px; color: #081C15">NEWS</h2>
      <div class="news-slider">
        <div class="news-cards">
          <div
              v-for="(news, idx) in visibleNews"
              :key="news.id"
              :class="['news-card', idx === 1 ? 'news-card--main' : 'news-card--blurred']"
          >
            <h3>
              <a
                  :href="news.url"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="news-link"
              >
                {{ news.title }}
              </a>
            </h3>
            <p>{{ news.description }}</p>

            <!-- Кнопки тільки на головній карточці -->
            <template v-if="idx === 1">
              <button class="arrow left" @click="prevNews" aria-label="Previous news">&#9664;</button>
              <button class="arrow right" @click="nextNews" aria-label="Next news">&#9654;</button>
            </template>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <p>Email: <a href="mailto:moneytalks@gmail.com">moneytalks_need_5@gmail.com</a></p>
      <div class="social-icons">
        <!-- Іконки Instagram і LinkedIn -->
        <i class="fab fa-instagram"></i>
        <i class="fab fa-linkedin"></i>
      </div>
    </footer>
  </div>
</template>

<script setup>
import {ref, computed, onMounted} from 'vue';
import axios from 'axios';

const newsItems = ref([]);
const currentIndex = ref(0);

const visibleNews = computed(() => {
  const len = newsItems.value.length;
  if (len < 3) return newsItems.value;

  const prevIndex = (currentIndex.value - 1 + len) % len;
  const nextIndex = (currentIndex.value + 1) % len;

  return [
    newsItems.value[prevIndex],
    newsItems.value[currentIndex.value],
    newsItems.value[nextIndex],
  ];
});

function prevNews() {
  currentIndex.value = (currentIndex.value - 1 + newsItems.value.length) % newsItems.value.length;
}

function nextNews() {
  currentIndex.value = (currentIndex.value + 1) % newsItems.value.length;
}

onMounted(async () => {
  try {
    const response = await axios.get("http://0.0.0.0:8000/api/v1/news/");
    newsItems.value = response.data;
  } catch (error) {
    console.error('Помилка при завантаженні новин:', error);
  }
});

const showAccountMenu = ref(false);

function toggleAccountMenu() {
  showAccountMenu.value = !showAccountMenu.value;
}
</script>

<style src="../assets/home.css"></style>
