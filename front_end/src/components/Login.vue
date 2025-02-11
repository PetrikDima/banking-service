<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <input v-model="username" type="text" placeholder="Username" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button type="submit">Login</button>
    </form>
    <p v-if="errorMessage">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { auth } from '../scripts/auth';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    };
  },
  methods: {
    async loginUser() {
      try {
        const data = await auth.login(this.username, this.password);
        console.log('Login successful:', data);
        if (auth.isAuthenticated) {
          localStorage.setItem('user-token', data.access);  // Додавання токену до сховища
          console.log('Redirecting to dashboard');
          this.$router.push('/dashboard');
        }
      } catch (error) {
        this.errorMessage = 'Invalid credentials';
        console.error('Login failed:', error);
      }
    }
  }
};
</script>
