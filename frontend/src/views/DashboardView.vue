<script setup>
import { useAuthStore } from '@/store/auth';
import { useExerciseStore } from '@/store/exercise';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const exerciseStore = useExerciseStore();
const router = useRouter();

const exercises = [
  { type: 'grammar', name: 'Gramer Kuralı', color: '#8854c7', description: 'Cümleleri doğru kelimelerle tamamla.' },
  { type: 'dialogue', name: 'Diyalog Tamamlama', color: '#4a90e2', description: 'Konuşmaları mantıklı bir şekilde ilerlet.', disabled: true },
  { type: 'word_matching', name: 'Kelime Eşleştirme', color: '#f5a623', description: 'Kelimeleri anlamlarıyla eşleştir.', disabled: true },
];

const startExercise = (exerciseType) => {
  router.push(`/exercise/${exerciseType}`);
};
</script>

<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Hoş Geldin, {{ authStore.user?.username }}!</h1>
      <div class="user-info">
        <router-link to="/leaderboard" class="leaderboard-link">🏆 Liderlik Tablosu</router-link>
        <span>Puan: <strong>{{ authStore.user?.weekly_score }}</strong></span>
        <button @click="authStore.logout()" class="btn btn-secondary">Çıkış Yap</button>
      </div>
    </header>

    <div v-if="exerciseStore.error" class="error-message">
      {{ exerciseStore.error }}
    </div>

    <div class="exercise-grid">
      <div
        v-for="exercise in exercises"
        :key="exercise.type"
        class="exercise-card"
        :class="{ disabled: exercise.disabled }"
        :style="{ borderTopColor: exercise.color }"
        @click="!exercise.disabled && startExercise(exercise.type)"
      >
        <h2>{{ exercise.name }}</h2>
        <p>{{ exercise.description }}</p>
        <span v-if="exercise.disabled" class="soon-badge">Yakında</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard { padding: 2rem; max-width: 900px; margin: 0 auto; }
.dashboard-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; flex-wrap: wrap; gap: 1rem; }
.user-info { display: flex; align-items: center; gap: 1.5rem; }
.leaderboard-link { text-decoration: none; background-color: var(--accent-color); color: white; padding: 0.6rem 1.2rem; border-radius: 20px; font-weight: 600; transition: background-color 0.2s; }
.leaderboard-link:hover { background-color: #d88e0f; }
.exercise-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }
.exercise-card { background: var(--surface-color); padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); border-top: 5px solid; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; }
.exercise-card:hover { transform: translateY(-5px); box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
.exercise-card.disabled { cursor: not-allowed; opacity: 0.6; position: relative; }
.soon-badge { position: absolute; top: 10px; right: 10px; background-color: var(--text-secondary); color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: bold; }
</style>
