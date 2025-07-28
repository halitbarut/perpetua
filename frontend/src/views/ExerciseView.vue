<script setup>
import { ref, computed, watch, onMounted } from 'vue';
import { useExerciseStore } from '@/store/exercise';
import { useRoute, useRouter } from 'vue-router';
import AppLoading from '@/components/AppLoading.vue';

const exerciseStore = useExerciseStore();
const router = useRouter();
const route = useRoute();

const selectedWord = ref(null);
const checkStatus = ref('unanswered');

const sentenceParts = computed(() => {
  const template = exerciseStore.currentQuestion?.sentence_template || '';
  return template.split('___');
});

const checkAnswer = () => {
  if (!selectedWord.value) return;
  if (selectedWord.value === exerciseStore.currentQuestion.correct_word) {
    checkStatus.value = 'correct';
  } else {
    checkStatus.value = 'incorrect';
  }
};

const nextStep = () => {
  exerciseStore.submitAnswer(selectedWord.value);
  selectedWord.value = null;
  checkStatus.value = 'unanswered';
};

watch(() => exerciseStore.currentQuestionIndex, () => {
  selectedWord.value = null;
  checkStatus.value = 'unanswered';
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

    <div class="question-panel">
      <h2>Cümleyi tamamla:</h2>
      <div class="sentence-box">
        <span>{{ sentenceParts[0] }}</span>
        <span class="word-slot" :class="{ filled: selectedWord }">{{ selectedWord }}</span>
        <span>{{ sentenceParts[1] }}</span>
      </div>
    </div>

    <div class="word-bank">
      <button
        v-for="word in exerciseStore.currentQuestion.word_bank"
        :key="word"
        class="word-button"
        @click="selectedWord = word"
        :disabled="checkStatus !== 'unanswered'"
      >
        {{ word }}
      </button>
    </div>

    <footer class="exercise-footer" :class="checkStatus">
      <div v-if="checkStatus === 'correct'" class="feedback-box">
        <h3>Harika!</h3>
      </div>
      <div v-if="checkStatus === 'incorrect'" class="feedback-box">
        <h3>Doğru Cevap: {{ exerciseStore.currentQuestion.correct_word }}</h3>
      </div>

      <button
        v-if="checkStatus === 'unanswered'"
        @click="checkAnswer"
        class="btn btn-primary"
        :disabled="!selectedWord"
      >
        Kontrol Et
      </button>
      <button
        v-else
        @click="nextStep"
        class="btn"
        :class="checkStatus === 'correct' ? 'btn-success' : 'btn-danger'"
      >
        Devam Et
      </button>
    </footer>
  </div>

  <div v-else-if="exerciseStore.isSessionFinished" class="results-container">
    <div class="results-card">
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
.exercise-container { display: flex; flex-direction: column; max-width: 600px; margin: 0 auto; padding: 2rem; height: calc(100vh - 4rem); justify-content: space-between; }
.progress-bar-container { width: 100%; background-color: var(--border-color); border-radius: 10px; height: 15px; }
.progress-bar { height: 100%; background-color: var(--primary-color); border-radius: 10px; transition: width 0.3s ease-in-out; }
.question-panel { text-align: center; margin: 2rem 0; }
.sentence-box { font-size: 1.8rem; margin-top: 1rem; background-color: var(--surface-color); padding: 2rem; border-radius: 12px; border: 1px solid var(--border-color); }
.word-slot { display: inline-block; min-width: 120px; border-bottom: 2px solid var(--border-color); margin: 0 10px; padding: 0 10px; height: 40px; line-height: 40px; font-weight: bold; color: var(--primary-color); }
.word-slot.filled { border-bottom-color: var(--primary-color); }
.word-bank { display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem; margin-bottom: 2rem; }
.word-button { padding: 1rem 2rem; font-size: 1.2rem; border: 2px solid var(--border-color); border-radius: 12px; background: var(--surface-color); cursor: pointer; transition: all 0.2s; }
.word-button:hover:not(:disabled) { background-color: #f1f3f5; border-color: #ccc; }
.word-button:disabled { opacity: 0.5; cursor: not-allowed; }
.exercise-footer { width: 100%; padding: 1.5rem 0; border-top: 2px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; transition: background-color 0.3s; }
.exercise-footer.correct { background-color: #d4edda; }
.exercise-footer.incorrect { background-color: #f8d7da; }
.feedback-box h3 { margin: 0; font-size: 1.2rem; }
.exercise-footer.correct h3 { color: #155724; }
.exercise-footer.incorrect h3 { color: #721c24; }
.btn-success { color: #fff; background-color: var(--success-color); border-color: var(--success-color); }
.btn-danger { color: #fff; background-color: var(--danger-color); border-color: var(--danger-color); }
.results-container { display: flex; justify-content: center; align-items: center; min-height: 100vh; }
.results-card { background-color: var(--surface-color); padding: 3rem; border-radius: 16px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); text-align: center; max-width: 500px; }
.final-score { color: var(--primary-color); font-size: 2.5rem; }
.feedback-ai { margin: 2rem 0; padding: 1.5rem; background: var(--background-color); border-left: 5px solid var(--primary-color); text-align: left; }
.feedback-ai p { font-style: italic; margin: 0 0 10px; }
.feedback-ai span { font-weight: bold; display: block; text-align: right; }
</style>
