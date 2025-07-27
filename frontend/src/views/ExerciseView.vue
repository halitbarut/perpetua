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
    console.error("Alıştırma tipi URL'de bulunamadı! Dashboard'a yönlendiriliyor.");
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
        class="check-btn"
        :disabled="!selectedWord"
      >
        Kontrol Et
      </button>
      <button
        v-else
        @click="nextStep"
        class="continue-btn"
      >
        Devam Et
      </button>
    </footer>
  </div>

  <div v-else-if="exerciseStore.isSessionFinished" class="results-container">
    <h1>Alıştırma Tamamlandı!</h1>
    <h2>Puanın: {{ exerciseStore.finalScore }}</h2>
    <div class="feedback-ai">
      <p>"{{ exerciseStore.finalFeedback }}"</p>
      <span>- Perpetua AI</span>
    </div>
    <button @click="router.push('/dashboard')" class="back-to-dashboard-btn">
      Harika, Geri Dön
    </button>
  </div>

</template>

<style scoped>
.exercise-container {
  display: flex;
  flex-direction: column;
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  height: 100vh;
  justify-content: space-between;
}
.progress-bar-container {
  width: 100%;
  background-color: #e0e0e0;
  border-radius: 10px;
  height: 15px;
}
.progress-bar {
  height: 100%;
  background-color: #5c6ac4;
  border-radius: 10px;
  transition: width 0.3s ease-in-out;
}
.question-panel {
  text-align: center;
  margin: 4rem 0;
}
.sentence-box {
  font-size: 1.8rem;
  margin-top: 1rem;
  background-color: #f7f7f7;
  padding: 2rem;
  border-radius: 12px;
}
.word-slot {
  display: inline-block;
  min-width: 120px;
  border-bottom: 2px solid #ccc;
  margin: 0 10px;
  padding: 0 10px;
  height: 40px;
  line-height: 40px;
  font-weight: bold;
  color: #5c6ac4;
}
.word-slot.filled {
  border-bottom: 2px solid #5c6ac4;
}
.word-bank {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}
.word-button {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  border: 2px solid #e0e0e0;
  border-radius: 12px;
  background: white;
  cursor: pointer;
  transition: all 0.2s;
}
.word-button:hover:not(:disabled) {
  background-color: #f0f2f5;
  border-color: #ccc;
}
.word-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.exercise-footer {
  width: 100%;
  padding: 1.5rem;
  margin: 0 -2rem -2rem;
  border-top: 2px solid #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: background-color 0.3s;
}
.exercise-footer.correct { background-color: #d4edda; }
.exercise-footer.incorrect { background-color: #f8d7da; }
.feedback-box h3 {
  margin: 0;
  font-size: 1.2rem;
}
.exercise-footer.correct h3 { color: #155724; }
.exercise-footer.incorrect h3 { color: #721c24; }
.check-btn, .continue-btn, .back-to-dashboard-btn {
  padding: 1rem 2rem;
  font-size: 1.2rem;
  border: none;
  border-radius: 12px;
  color: white;
  background-color: #5c6ac4;
  cursor: pointer;
}
.check-btn:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}
.continue-btn {
  background-color: #4caf50;
}
.exercise-footer.incorrect .continue-btn {
  background-color: #f44336;
}
.results-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  text-align: center;
}
.feedback-ai {
  margin: 2rem 0;
  padding: 1.5rem;
  background: #f7f7f7;
  border-left: 5px solid #5c6ac4;
  max-width: 500px;
}
.feedback-ai p {
  font-style: italic;
  margin: 0 0 10px;
}
.feedback-ai span {
  font-weight: bold;
}
</style>
