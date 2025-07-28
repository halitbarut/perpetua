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
    // Yönlendirme store içinde yapılıyor
  } catch (err) {
    error.value = err.detail || 'Kayıt başarısız oldu.';
  }
};
</script>

<template>
  <div class="auth-page">
    <div class="auth-form">
      <h1>Kayıt Ol</h1>
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

<!-- LoginView.vue ve RegisterView.vue için yeni <style> -->
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
}
p {
  margin-top: 1.5rem;
}
</style>
