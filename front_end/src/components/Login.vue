<template>
  <link href="https://fonts.googleapis.com/css2?family=Poppins&display=swap" rel="stylesheet">
  <div class="login-wrapper">
    <div class="close-button" @click="closeForm">&times;</div>

    <div class="login-header">
      <h1>Log In</h1>
      <p>Welcome back! Please enter your credentials to access your account.</p>
    </div>

    <div class="input-form">
      <div class="input-group">
        <input v-model="username" type="email" placeholder="Email" required/>
      </div>
      <div class="input-group password-wrapper">
        <input :type="showPassword ? 'text' : 'password'" v-model="password" placeholder="Password" required/>
        <img
            v-if="showPassword"
            src="@/assets/icons/eye-off.png"
            alt="Hide Password"
            class="toggle-visibility"
            @click="togglePassword"
        />
        <img
            v-else
            src="@/assets/icons/eye-on.png"
            alt="Show Password"
            class="toggle-visibility"
            @click="togglePassword"
        />
      </div>
    </div>

    <button class="login-button" @click="loginUser">Log In</button>

    <div class="bottom-link" @click="signIn">Sign Up</div>

    <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
  </div>
</template>

<script>
import {auth} from '../scripts/auth';

export default {
  data() {
    return {
      username: '',
      password: '',
      showPassword: false,
      errorMessage: ''
    };
  },
  methods: {
    async loginUser() {
      try {
        const data = await auth.login(this.username, this.password);
        localStorage.setItem('user-token', data.access);
        this.$router.push('/home');
      } catch (err) {
        this.errorMessage = '';
      }
    },
    togglePassword() {
      this.showPassword = !this.showPassword;
    },
    signIn() {
      this.$router.push('/register');
    },
    closeForm() {
      this.$emit('close');
    }
  }
};
</script>

<style scoped>
body {
  font-family: 'Poppins', sans-serif;
}

.login-wrapper {
  width: 566px;
  height: 519px;
  border-radius: 30px;
  background: linear-gradient(230deg, #ffffff 30%, #7AAD85 100%);
  padding: 0;
  margin: 100px auto;
  position: relative;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
  overflow: hidden;
}

.login-header {
  position: absolute;
  top: 64px;
  left: 64px;
  width: 438px;
  height: 123px;
}

.login-header h1 {
  font-size: 36px;
  margin: 0 0 10px 0;
  color: #1a1a1a;
  font-weight: 400;
  font-family: 'Poppins', sans-serif
}

.login-header p {
  color: #6c6c6c;
  font-size: 16px;
  margin: 0;
}

.input-form {
  position: absolute;
  top: 212px;
  left: 64px;
  width: 444px;
}

.input-group {
  margin-bottom: 16px;
}

.input-group input {
  width: 100%;
  padding: 15px 20px;
  border-radius: 10px;
  border: 1px solid #808080;
  font-size: 16px;
  box-sizing: border-box;
  background: transparent;
  font-family: 'Poppins', sans-serif;
  color: #1a1a1a;
}

.input-group input:focus {
  outline: none;
  border-color: #7AAD85;
  box-shadow: 0 0 0 2px rgba(122, 173, 133, 0.2);
}

.password-wrapper {
  position: relative;
}

.password-wrapper .toggle-visibility {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  cursor: pointer;
}

.password-wrapper img {
  width: 20px;
  height: 20px;
  cursor: pointer;
}

.login-button {
  position: absolute;
  top: 374px;
  left: 64px;
  width: 438px;
  height: 52px;
  border-radius: 30px;
  background-color: #1c2b18;
  color: #DBFEB8;
  font-size: 16px;
  border: none;
  cursor: pointer;
  line-height: 52px;
  font-weight: 300;
  font-family: 'Poppins', sans-serif;
  text-align: center;
  padding: 0;
}

.bottom-link {
  position: absolute;
  top: 453px;
  left: 247px;
  width: 71px;
  height: 36px;
  text-align: center;
  color: #1a1a1a;
  font-size: 18px;
  cursor: pointer;
  font-family: 'Poppins', sans-serif;
}

.error-text {
  position: absolute;
  top: 440px;
  left: 64px;
  color: red;
}

.close-button {
  position: absolute;
  top: 20px;
  right: 20px;
  width: 2px;
  height: 2px;
  font-size: 32px;
  text-align: center;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.2s;
  color: #000;
}

.close-button:hover {
  background: rgba(0, 0, 0, 0.1);
}

.input-group input::placeholder {
  color: #1a1a1a;
  opacity: 1;
}
</style>