<!-- frontend/src/views/ExerciseView.vue -->
<script setup>
import { computed, onMounted } from 'vue';
import { useExerciseStore } from '@/store/exercise';
import { useRoute, useRouter } from 'vue-router';
import AppLoading from '@/components/AppLoading.vue';
import GrammarExercise from '@/components/exercises/GrammarExercise.vue';
import DialogueExercise from '@/components/exercises/DialogueExercise.vue';
import WordMatchingExercise from '@/components/exercises/WordMatchingExercise.vue';

const exerciseStore = useExerciseStore();
const router = useRouter();
const route = useRoute();

const exerciseComponents = {
  grammar: GrammarExercise,
  dialogue: DialogueExercise,
  word_matching: WordMatchingExercise,
};

const currentExerciseComponent = computed(() => {
  if (!exerciseStore.isSessionActive || exerciseStore.questions.length === 0) {
    return null;
  }
  const currentType = exerciseStore.questions[0]?.type;
  return exerciseComponents[currentType] || null;
});

onMounted(async () => {
  const exerciseType = route.params.type;
  if (!exerciseType) {
    router.push('/dashboard');
    return;
  }
  await exerciseStore.startNewSession(exerciseType);
  if (exerciseStore.error) {
    router.push('/dashboard');
  }
});
</script>

<template>
  <AppLoading
    v-if="exerciseStore.isLoading"
    :title="exerciseStore.isSessionFinished ? 'Sonuçlar Değerlendiriliyor...' : 'Alıştırma Hazırlanıyor...'"
  />

  <div v-else-if="exerciseStore.isSessionActive && !exerciseStore.isSessionFinished" class="exercise-container">
    <div class="progress-bar-container">
      <div class="progress-bar" :style="{ width: `${(exerciseStore.currentQuestionIndex / exerciseStore.questions.length) * 100}%` }"></div>
    </div>

    <component :is="currentExerciseComponent" v-if="currentExerciseComponent" />
    <div v-else class="loading-component">
      Alıştırma bileşeni yükleniyor...
    </div>
  </div>

  <div v-else-if="exerciseStore.isSessionFinished" class="results-container">
    <div class="results-card">
      <transition name="fade" mode="out-in">
        <component :is="currentExerciseComponent" :key="exerciseStore.currentQuestionIndex" />
      </transition>
      <h1>Alıştırma Tamamlandı!</h1>
      <h2>Puanın: <span class="final-score">{{ exerciseStore.finalScore }}</span></h2>
      <div class="feedback-ai">
        <p>"{{ exerciseStore.finalFeedback }}"</p>
        <span>- Perpetua AI</span>
      </div>
      <button @click="router.push('/dashboard')" class="btn btn-primary">
        Harika, Geri Dön
      </button>
    </div>
  </div>
</template>

<style scoped>
.exercise-container { display: flex; flex-direction: column; max-width: 600px; margin: 0 auto; padding: 2rem; min-height: 100vh; box-sizing: border-box; }
.progress-bar-container { width: 100%; background-color: var(--border-color); border-radius: 10px; height: 15px; margin-bottom: 1rem; }
.progress-bar { height: 100%; background-color: var(--primary-color); border-radius: 10px; transition: width 0.3s ease-in-out; }
.results-container { display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.results-card { background-color: var(--surface-color); padding: 3rem; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); text-align: center; max-width: 500px; }
.final-score { color: var(--primary-color); font-size: 2.5rem; }
.feedback-ai { margin: 2rem 0; padding: 1.5rem; background: var(--background-color); border-left: 5px solid var(--primary-color); text-align: left; }
.feedback-ai p { font-style: italic; margin: 0 0 10px; }
.feedback-ai span { font-weight: bold; display: block; text-align: right; }
.loading-component { flex-grow: 1; display: flex; justify-content: center; align-items: center; color: var(--text-secondary); }
</style>
