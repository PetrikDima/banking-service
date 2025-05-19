<template>
  <div class="container">
    <!-- Top Nav -->
    <img src="../assets/money_talks_background.jpg" alt="background" class="background-image">
    <header class="header">
      <nav class="nav">
        <a href="#">Home</a>
        <a href="#">Cards</a>
        <a href="#">Investments</a>
      </nav>
      <div class="header-buttons">
        <button><img src="../assets/icons/messages.svg" alt="messages"></button>
        <button><img src="../assets/icons/accout_icon.svg" alt="account"></button>
      </div>
    </header>

    <!-- Info Section -->
    <section class="info-section">
      <div class="info-about-company">
        <div class="info-text-block">
          <h1>Info about company</h1>
          <p>
            This personal finance planning service is a side project by two friends aiming to help users better manage their money. It allows tracking income and expenses, setting financial goals, and analyzing spending habits through clear visualizations. Built with Django (DRF), Vue.js, and PostgreSQL, it also supports banking API integrations like Monobank for automatic transaction syncing.
          </p>
          <button class="btn-primary">Read more &gt;</button>
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
            <h3>{{ news.title }}</h3>
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
import {ref, computed} from 'vue';

const newsItems = ref([
  {id: 1, title: 'News 1', description: 'Lorem ipsum dolor sit amet consectetur.'},
  {id: 2, title: 'News 2', description: 'Quis urna mattis adipiscing in habitant platea sed libero.'},
  {id: 3, title: 'News 3', description: 'Lorem ipsum dolor sit amet consectetur.'},
  {id: 4, title: 'News 4', description: 'Vivamus luctus urna sed urna ultricies.'},
  {id: 5, title: 'News 5', description: 'Praesent dapibus, neque id cursus faucibus.'},
  {id: 6, title: 'News 6', description: 'Phasellus nec sem in justo pellentesque.'},
  {id: 7, title: 'News 7', description: 'Fusce nec tellus sed augue semper.'},
  {id: 8, title: 'News 8', description: 'Donec vitae sapien ut libero venenatis.'},
  {id: 9, title: 'News 9', description: 'Nullam quis ante. Etiam sit amet orci.'},
  {id: 10, title: 'News 10', description: 'Suspendisse potenti. Sed lectus.'},
]);

const currentIndex = ref(0);

const visibleNews = computed(() => {
  const len = newsItems.value.length;
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
</script>

<style scoped>
/* Основний контейнер */
.container {
  width: 100%;
  display: flex;
  flex-direction: column;
  color: #1f2937;
  font-family: sans-serif;
  position: relative;
  overflow: hidden;
  padding: 0;
  margin: 0;
}

.background-image {
  position: absolute;
  top: 0;
  left: 0;
  height: 875px;
  width: 100%;
  z-index: -1;
  pointer-events: none;
  background-repeat: no-repeat;
  background-size: 100% 100%, cover;
  /*transform: rotate(180deg);*/
  transform: scaleY(-1) rotate(180deg);
}
/* Хедер */
.header {
  width: 100%;
  height: 97px;
  display: flex;
  align-items: center;
  gap: 1035px;
  padding: 0 3rem;
}

.nav {
  display: flex;
  gap: 2rem;
  font-size: 1rem;
  align-items: center;
}

.nav a {
  color: #081C15;
  text-decoration: none;
  transition: color 0.2s;
  font-size: 20px;
}

.nav a:hover {
  color: #059669;
}

.header-buttons {
  display: flex;
  gap: 1rem;
}

.header-buttons button {
  background: none;
  border: none;
  font-size: 1.25rem;
  color: #374151;
  cursor: pointer;
  transition: color 0.2s;
}

.header-buttons button:hover {
  color: #059669;
}

/* Блок інформації */
.info-section {
  width: 100%;
  height: 875px;
  position: relative;
  margin-top: 65px;
}

.money-image-wrapper {
  position: relative;
  width: 100%;
  height: 875px;
  overflow: visible;
}

.money-image-wrapper img {
  width: 100%;
  height: 875px;
  transform: rotate(-180deg);
  object-fit: cover;
  display: block;
}

.info-about-company {
  position: absolute;
  top: 259px;
  left: 36px;
  width: 544px;
  height: 419px;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
}

.info-text-block {
  width: 508px;
  padding: 1rem;
  color: #000000;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 8px;
}

.info-text-block h1 {
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
}

.info-text-block p {
  font-size: 1.125rem;
  line-height: 1.5rem;
  flex-grow: 1;
}

.btn-primary {
  background-color: #000000;
  color: #dbfeb8;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  border: none;
  cursor: pointer;
  align-self: flex-start;
  margin-top: 1rem;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.btn-primary:hover {
  background-color: #065f46;
}

/* Блок новин */
.news-section {
  width: 100%;
  padding: 4rem 3rem;
  background-color: white;
  margin-top: -150px;
}

.news-section h2 {
  text-align: center;
  font-weight: 700;
  font-size: 1.5rem;
  margin-bottom: 3rem;
  color: #065f46;
}

.news-cards {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  position: relative;
}

.news-card {
  border-radius: 34px;
  padding: 1.5rem;
  width: 576px;
  height: 390px;
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
  background-color: #2d6a4f;
  color: #dbfeb8;
  font-size: 1rem;
  position: relative;
  transition: filter 0.3s, opacity 0.3s, transform 0.3s;
  flex-shrink: 0;
  user-select: none;
}

.news-card--main {
  filter: none;
  opacity: 1;
  transform: scale(1);
  z-index: 5;
}

.news-card--blurred {
  filter: blur(3px);
  opacity: 0.6;
  transform: scale(0.9);
  z-index: 1;
}

.arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  font-size: 2.5rem;
  color: #dbfeb8;
  cursor: pointer;
  user-select: none;
  transition: color 0.3s;
  z-index: 10;
  padding: 0 0.25rem;
  width: 40px;
  height: 100px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 0.5rem;
}

.arrow:hover {
  color: #aee2b6;
}

.arrow.left {
  left: -50px;
}

.arrow.right {
  right: -50px;
}

/* Футер */
.footer {
  width: 100%;
  height: 60px;
  background: linear-gradient(to top, #2d6a4f, #8ba39400);
  color: white;
  padding: 1rem 3rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: auto;
}

.footer p a {
  color: #dbfeb8;
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
</style>
