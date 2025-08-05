<!-- frontend/src/components/exercises/DialogueExercise.vue (DOĞRULANMIŞ) -->
<script setup>
import { ref, watch } from 'vue';
import { useExerciseStore } from '@/store/exercise';

const exerciseStore = useExerciseStore();
const selectedOption = ref(null);
const checkStatus = ref('unanswered');

const checkAnswer = () => {
  if (!selectedOption.value) return;
  if (selectedOption.value === exerciseStore.currentQuestion.correct_answer) {
    checkStatus.value = 'correct';
  } else {
    checkStatus.value = 'incorrect';
  }
};

const nextStep = () => {
  exerciseStore.submitAnswer(selectedOption.value);
  selectedOption.value = null;
  checkStatus.value = 'unanswered';
};

watch(() => exerciseStore.currentQuestionIndex, () => {
  selectedOption.value = null;
  checkStatus.value = 'unanswered';
});
</script>

<template>
  <!-- ANA VE TEK TEMPLATE ETİKETİ BAŞLANGICI -->
  <div class="exercise-wrapper">
    <div class="exercise-content">
      <div class="dialogue-box">
        <div v-for="(line, index) in exerciseStore.currentQuestion.dialogue" :key="index" class="dialogue-line">
          <strong>{{ line.speaker }}:</strong> "{{ line.line }}"
        </div>
      </div>

      <div class="question-panel">
        <h2>{{ exerciseStore.currentQuestion.question }}</h2>
      </div>

      <div class="options-grid">
        <button
          v-for="option in exerciseStore.currentQuestion.options"
          :key="option"
          class="option-button"
          @click="selectedOption = option"
          :class="{ selected: selectedOption === option }"
          :disabled="checkStatus !== 'unanswered'"
        >
          {{ option }}
        </button>
      </div>
    </div>

    <footer class="exercise-footer" :class="checkStatus">
      <div v-if="checkStatus === 'correct'" class="feedback-box">
        <h3>Doğru!</h3>
      </div>
      <div v-if="checkStatus === 'incorrect'" class="feedback-box">
        <h3>Doğru Cevap: {{ exerciseStore.currentQuestion.correct_answer }}</h3>
      </div>

      <button
        v-if="checkStatus === 'unanswered'"
        @click="checkAnswer"
        class="btn btn-primary"
        :disabled="!selectedOption"
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
/* Stilleri tek bir div içinde sarmalayarak daha iyi yönetelim */
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
.dialogue-box {
  background-color: var(--surface-color);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.5rem;
  margin-bottom: 2rem;
}
.dialogue-line { margin-bottom: 0.75rem; font-size: 1.1rem; }
.question-panel h2 { text-align: center; margin-bottom: 2rem; }
.options-grid { display: grid; grid-template-columns: 1fr; gap: 1rem; }
.option-button { width: 100%; padding: 1rem; font-size: 1rem; text-align: left; border: 2px solid var(--border-color); border-radius: 12px; background-color: var(--surface-color); cursor: pointer; }
.option-button.selected { border-color: var(--primary-color); background-color: #eaf2fd; }
.option-button:disabled { opacity: 0.6; cursor: not-allowed; }

.exercise-footer { width: 100%; padding: 1.5rem 2rem; border-top: 2px solid var(--border-color); display: flex; align-items: center; justify-content: space-between; transition: background-color 0.3s; box-sizing: border-box; }
.exercise-footer.correct { background-color: #d4edda; }
.exercise-footer.incorrect { background-color: #f8d7da; }
.feedback-box h3 { margin: 0; font-size: 1.2rem; }
.exercise-footer.correct h3 { color: #155724; }
.exercise-footer.incorrect h3 { color: #721c24; }
.btn-success { color: #fff; background-color: var(--success-color); border-color: var(--success-color); }
.btn-danger { color: #fff; background-color: var(--danger-color); border-color: var(--danger-color); }
</style>
