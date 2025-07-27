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
        <span>Haftalık Puanın: {{ authStore.user?.weekly_score }}</span>
        <button @click="authStore.logout()" class="logout-btn">Çıkış Yap</button>
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
/* Stil kodları aynı */
.dashboard {
  padding: 2rem;
  max-width: 900px;
  margin: 0 auto;
}
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}
.user-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}
.logout-btn {
  padding: 0.5rem 1rem;
  border: 1px solid #ccc;
  background: transparent;
  cursor: pointer;
  border-radius: 4px;
}
.exercise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}
.exercise-card {
  background: white;
  padding: 1.5rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
  border-top: 5px solid;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}
.exercise-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0,0,0,0.1);
}
.exercise-card.disabled {
  cursor: not-allowed;
  opacity: 0.6;
  position: relative;
}
.exercise-card.disabled:hover {
  transform: none;
  box-shadow: 0 4px 10px rgba(0,0,0,0.05);
}
.soon-badge {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #777;
  color: white;
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 0.75rem;
  font-weight: bold;
}
.error-message {
  background-color: #ffdddd;
  color: #d8000c;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  text-align: center;
}
</style>
