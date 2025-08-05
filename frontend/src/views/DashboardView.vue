<script setup>
import {ref, onMounted} from 'vue';
import {useAuthStore} from '@/store/auth';
import {useExerciseStore} from '@/store/exercise';
import {useRouter} from 'vue-router';
import {userService} from '@/services/user.service';

const authStore = useAuthStore();
const exerciseStore = useExerciseStore();
const router = useRouter();

const aiFeedback = ref(null);
const isLoadingFeedback = ref(true);
const levels = ['A1', 'A2', 'B1', 'B2'];
const isSavingLevel = ref(false);

const exercises = [
  {
    type: 'grammar',
    name: 'Gramer Kuralı',
    color: '#8854c7',
    description: 'Cümleleri doğru kelimelerle tamamla.'
  },
  {
    type: 'dialogue',
    name: 'Diyalog Tamamlama',
    color: '#4a90e2',
    description: 'Konuşmaları mantıklı bir şekilde ilerlet.'
  },
  {
    type: 'word_matching',
    name: 'Kelime Eşleştirme',
    color: '#f5a623',
    description: 'Kelimeleri anlamlarıyla eşleştir.'
  },
];

const startExercise = (exerciseType) => {
  router.push(`/exercise/${exerciseType}`);
};

const changeLevel = async (newLevel) => {
  if (isSavingLevel.value || newLevel === authStore.user?.current_level) return;
  isSavingLevel.value = true;
  try {
    await userService.updateUserLevel(newLevel);
    await authStore.fetchCurrentUser();
  } catch (error) {
    console.error("Seviye güncellenemedi:", error);
  } finally {
    isSavingLevel.value = false;
  }
};

onMounted(async () => {
  try {
    const {data} = await userService.getAIFeedback();
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
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="brand">
        <img src="@/assets/logo.png" alt="Perpetua Logo" class="header-logo"/>
        <h1>Perpetua</h1>
      </div>
      <div class="user-controls">
        <div class="level-selector">
          <button
            v-for="level in levels"
            :key="level"
            class="level-btn"
            :class="{ active: authStore.user?.current_level === level }"
            @click="changeLevel(level)"
            :disabled="isSavingLevel"
          >
            {{ level }}
          </button>
        </div>
        <router-link to="/leaderboard" class="leaderboard-link" title="Liderlik Tablosu">🏆
        </router-link>

        <!-- YENİ YAPI: ÇIKIŞ BUTONU user-info'nun İÇİNE GİRDİ -->
        <div class="user-info">
          <div class="user-details">
            <span>{{ authStore.user?.username }}</span>
            <small>Puan: <strong>{{ authStore.user?.weekly_score }}</strong></small>
          </div>
          <button @click="authStore.logout()" class="logout-btn" title="Çıkış Yap">🚪</button>
        </div>

      </div>
    </header>

    <main class="dashboard-content">
      <div class="ai-feedback-card">
        <div class="ai-feedback-header">🤖 AI Koçundan Tavsiye</div>
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
          @click="startExercise(exercise.type)"
          :style="{ borderTopColor: exercise.color }"
        >
          <h2>{{ exercise.name }}</h2>
          <p>{{ exercise.description }}</p>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 2rem;
}

.dashboard-header {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 0;
  border-bottom: 1px solid var(--border-color);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-logo {
  height: 40px;
}

.brand h1 {
  font-size: 1.5rem;
  margin: 0;
}

.user-controls {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.level-selector {
  display: flex;
  background-color: #e9ecef;
  border-radius: 8px;
  padding: 4px;
}

.level-btn {
  border: none;
  background-color: transparent;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  color: var(--text-secondary);
}

.level-btn.active {
  background-color: var(--surface-color);
  color: var(--primary-color);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.leaderboard-link {
  font-size: 1.8rem;
  text-decoration: none;
  color: var(--text-secondary);
  transition: transform 0.2s;
}

.leaderboard-link:hover {
  transform: scale(1.2);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  background-color: #f8f9fa;
  padding: 0.5rem 0.5rem 0.5rem 1rem;
  border-radius: 8px;
  border: 1px solid var(--border-color);
}

.user-details {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  line-height: 1.2;
}

.user-details span {
  font-weight: 600;
}

.user-details small {
  color: var(--text-secondary);
}

.logout-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 6px;
  line-height: 1;
  transition: background-color 0.2s;
}

.logout-btn:hover {
  background-color: #e9ecef;
}

.user-info span {
  font-weight: 600;
}

.user-info small {
  color: var(--text-secondary);
}

.logout-btn {
  padding: 0.5rem 1rem;
}

.dashboard-content {
  padding: 2.5rem 0;
}

.ai-feedback-card {
  background: linear-gradient(135deg, #eaf2fd 0%, #e6e9f0 100%);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  margin-bottom: 2.5rem;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.ai-feedback-header {
  font-weight: 600;
  padding: 0.75rem 1.5rem;
  background-color: rgba(255, 255, 255, 0.5);
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
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
}

.exercise-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.exercise-card {
  background: var(--surface-color);
  padding: 1.5rem;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
  border-top: 5px solid;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.exercise-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  text-align: center;
}

.dashboard-content {
  padding: 2.5rem 0;
}
</style>
