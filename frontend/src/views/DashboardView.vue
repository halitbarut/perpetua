<!-- frontend/src/views/DashboardView.vue -->
<script setup>
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/store/auth';
import { useExerciseStore } from '@/store/exercise';
import { useRouter } from 'vue-router';
import { userService } from '@/services/user.service'; // user.service'i import et

const authStore = useAuthStore();
const exerciseStore = useExerciseStore();
const router = useRouter();

const aiFeedback = ref(null);
const isLoadingFeedback = ref(true);

const exercises = [
  { type: 'grammar', name: 'Gramer Kuralı', color: '#8854c7', description: 'Cümleleri doğru kelimelerle tamamla.' },
  { type: 'dialogue', name: 'Diyalog Tamamlama', color: '#4a90e2', description: 'Konuşmaları mantıklı bir şekilde ilerlet.' },
  { type: 'word_matching', name: 'Kelime Eşleştirme', color: '#f5a623', description: 'Kelimeleri anlamlarıyla eşleştir.' },
];

const startExercise = (exerciseType) => {
  router.push(`/exercise/${exerciseType}`);
};

onMounted(async () => {
  try {
    const { data } = await userService.getAIFeedback();
    aiFeedback.value = data;
  } catch (error) {
    console.error("AI tavsiyesi alınamadı:", error);
    aiFeedback.value = "Şu anda senin için özel bir tavsiye hazırlayamadım, ama harika gittiğini biliyorum!";
  } finally {
    isLoadingFeedback.value = false;
  }
});
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

    <div class="ai-feedback-card">
      <div class="ai-feedback-header">
        🤖 AI Koçundan Tavsiye
      </div>
      <div class="ai-feedback-body">
        <p v-if="isLoadingFeedback">Senin için kişisel bir tavsiye hazırlanıyor...</p>
        <p v-else>{{ aiFeedback }}</p>
      </div>
    </div>

    <div v-if="exerciseStore.error" class="error-message">
      {{ exerciseStore.error }}
    </div>

    <h2 class="section-title">Alıştırmalar</h2>
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
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard { padding: 2rem; max-width: 900px; margin: 0 auto; }
.dashboard-header { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; margin-bottom: 2rem; gap: 1rem; }
.dashboard-header h1 { margin: 0; }
.user-info { display: flex; align-items: center; gap: 1.5rem; }
.leaderboard-link { text-decoration: none; background-color: var(--accent-color); color: white; padding: 0.6rem 1.2rem; border-radius: 20px; font-weight: 600; transition: background-color 0.2s; white-space: nowrap; }
.leaderboard-link:hover { background-color: #d88e0f; }
.exercise-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; }
.exercise-card { background: var(--surface-color); padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.06); border-top: 5px solid; cursor: pointer; transition: transform 0.2s, box-shadow 0.2s; position: relative; }
.exercise-card:hover { transform: translateY(-5px); box-shadow: 0 6px 20px rgba(0,0,0,0.08); }
.exercise-card.disabled { cursor: not-allowed; opacity: 0.6; }
.exercise-card.disabled:hover { transform: none; box-shadow: 0 4px 15px rgba(0,0,0,0.06); }
.soon-badge { position: absolute; top: 10px; right: 10px; background-color: var(--text-secondary); color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.75rem; font-weight: bold; }
.error-message { background-color: #f8d7da; color: #721c24; padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem; text-align: center; }
.ai-feedback-card {
  background: linear-gradient(135deg, #eaf2fd 0%, #e6e9f0 100%);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  margin-bottom: 2.5rem;
  box-shadow: 0 4px 15px rgba(0,0,0,0.05);
}
.ai-feedback-header {
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  background-color: rgba(255,255,255,0.5);
  border-bottom: 1px solid var(--border-color);
  border-radius: 12px 12px 0 0;
}
.ai-feedback-body {
  padding: 1.5rem;
  font-size: 1.1rem;
  font-style: italic;
  color: #34495e;
}
.ai-feedback-body p {
  margin: 0;
  color: #34495e;
}
.section-title {
  margin-top: 2.5rem;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}
</style>
