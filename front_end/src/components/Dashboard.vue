<template>
  <div>
    <h2>Welcome to the Dashboard</h2>
    <button @click="logout">Logout</button>
  </div>
</template>

<script>
import { auth } from '../scripts/auth';

export default {
  methods: {
    logout() {
      auth.logout();
      this.$router.push('/login');
    }
  }
};
</script>
