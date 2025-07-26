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
        <button type="submit" class="btn">Kayıt Ol</button>
      </form>
      <p>
        Zaten bir hesabın var mı?
        <router-link to="/login">Giriş Yap</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
/* Stiller Login.vue ile aynı olduğu için kopyalayabiliriz veya global yapabiliriz */
/* Şimdilik kolaylık olması için kopyalıyorum */
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
