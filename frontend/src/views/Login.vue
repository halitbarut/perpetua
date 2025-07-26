<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const error = ref(null);

const handleLogin = async () => {
  error.value = null;
  try {
    await authStore.login({ username: email.value, password: password.value });
  } catch (err) {
    error.value = err.detail || 'Giriş yapılamadı. Lütfen bilgilerinizi kontrol edin.';
  }
};
</script>

<template>
  <div class="auth-page">
    <div class="auth-form">
      <h1>Giriş Yap</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label for="email">E-posta</label>
          <input type="email" id="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label for="password">Şifre</label>
          <input type="password" id="password" v-model="password" required />
        </div>
        <div v-if="error" class="error-message">{{ error }}</div>
        <button type="submit" class="btn">Giriş Yap</button>
      </form>
      <p>
        Hesabın yok mu?
        <router-link to="/register">Kayıt Ol</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f0f2f5;
}
.auth-form {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}
.form-group {
  margin-bottom: 1rem;
  text-align: left;
}
label {
  display: block;
  margin-bottom: 0.5rem;
}
input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.btn {
  width: 100%;
  padding: 0.75rem;
  border: none;
  background-color: #5c6ac4;
  color: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}
.error-message {
  color: red;
  margin-bottom: 1rem;
}
</style>
