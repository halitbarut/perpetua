<script setup>
import { ref } from 'vue';
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();

const username = ref('');
const email = ref('');
const password = ref('');
const error = ref(null);

const handleRegister = async () => {
  error.value = null;
  if (password.value.length < 6) {
    error.value = 'Şifre en az 6 karakter olmalıdır.';
    return;
  }
  try {
    await authStore.register({
      username: username.value,
      email: email.value,
      password: password.value,
    });
  } catch (err) {
    error.value = err.detail || 'Kayıt başarısız oldu. Lütfen bilgileri kontrol edin veya farklı bir kullanıcı adı/e-posta deneyin.';
  }
};
</script>

<template>
  <div class="auth-page">
    <div class="auth-form">
      <img src="@/assets/logo.png" alt="Perpetua Logo" class="logo" />
      <h1>Hesap Oluştur</h1>
      <p class="subtitle">Macerana katılmak için sadece bir adım kaldı.</p>

      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label for="username">Kullanıcı Adı</label>
          <input type="text" id="username" v-model="username" required />
        </div>
        <div class="form-group">
          <label for="email">E-posta</label>
          <input type="email" id="email" v-model="email" required />
        </div>
        <div class="form-group">
          <label for="password">Şifre</label>
          <input type="password" id="password" v-model="password" required />
        </div>

        <div v-if="error" class="error-message">{{ error }}</div>

        <button type="submit" class="btn btn-primary">Kayıt Ol</button>
      </form>

      <p>
        Zaten bir hesabın var mı?
        <router-link to="/login">Giriş Yap</router-link>
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
