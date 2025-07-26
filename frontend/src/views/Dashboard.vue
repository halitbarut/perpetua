<script setup>
import { useAuthStore } from '@/store/auth';

const authStore = useAuthStore();
</script>

<template>
  <div>
    <h1>Hoş Geldin, {{ authStore.user?.username }}!</h1>
    <p>Perpetua'ya hoş geldin. Alıştırmalara başlamak için hazır mısın?</p>
    <p>Haftalık Puanın: {{ authStore.user?.weekly_score }}</p>
    <button @click="authStore.logout()">Çıkış Yap</button>
  </div>
</template>

<style scoped>
h1 {
  color: #333;
}
</style>
