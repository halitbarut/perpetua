<!-- frontend/src/components/exercises/GrammarExercise.vue (DOĞRULANMIŞ) -->
<script setup>
// Script kısmı zaten doğruydu, aynı kalıyor
import { ref, computed, watch } from 'vue';
import { useExerciseStore } from '@/store/exercise';

const exerciseStore = useExerciseStore();
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
</script>

<template>
  <!-- ANA VE TEK TEMPLATE ETİKETİ BAŞLANGICI -->
  <div class="exercise-wrapper">
    <div class="exercise-content">
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
  <!-- ANA VE TEK TEMPLATE ETİKETİ BİTİŞİ -->
</template>

<style scoped>
.exercise-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}
.exercise-content {
  width: 100%;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.question-panel { text-align: center; margin: 2rem 0; }
.sentence-box { font-size: 1.8rem; margin-top: 1rem; background-color: var(--surface-color); padding: 2rem; border-radius: 12px; border: 1px solid var(--border-color); }
.word-slot { display: inline-block; min-width: 120px; border-bottom: 2px solid var(--border-color); margin: 0 10px; padding: 0 10px; height: 40px; line-height: 40px; font-weight: bold; color: var(--primary-color); }
.word-slot.filled { border-bottom-color: var(--primary-color); }
.word-bank { display: flex; flex-wrap: wrap; justify-content: center; gap: 1rem; margin-top: 2rem; padding-bottom: 2rem; }
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
</style>
