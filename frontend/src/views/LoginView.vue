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
      <img src="@/assets/logo.png" alt="Perpetua Logo" class="logo" />
      <h1>Perpetua'ya Hoş Geldin</h1>
      <p class="subtitle">AI destekli dil öğrenme maceran başlasın.</p>

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
        <button type="submit" class="btn btn-primary">Giriş Yap</button>
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
}
.auth-form {
  background: var(--surface-color);
  padding: 2.5rem;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.05);
  width: 100%;
  max-width: 400px;

  display: flex;
  flex-direction: column;
  align-items: stretch;
}

.logo {
  height: 60px;
  margin-bottom: 1rem;
  align-self: center;
}

h1 {
  margin-bottom: 0.5rem;
  text-align: center;
}

.subtitle {
  margin-top: 0;
  margin-bottom: 2rem;
  color: var(--text-secondary);
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input {
  box-sizing: border-box;
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  font-size: 1rem;
}

input:focus {
  outline: none;
  border-color: var(--primary-color);
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.25);
}

.error-message {
  color: var(--danger-color);
  margin-bottom: 1rem;
  text-align: center;
}

.btn-primary {
  width: 100%;
}

p {
  margin-top: 1.5rem;
  text-align: center;
}
</style>
