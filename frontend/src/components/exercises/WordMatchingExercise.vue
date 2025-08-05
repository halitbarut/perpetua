<script setup>
import {ref, computed, watch} from 'vue';
import {useExerciseStore} from '@/store/exercise';

const exerciseStore = useExerciseStore();

const selectedWord = ref(null);
const selectedMeaning = ref(null);
const correctlyMatchedPairs = ref([]);
const incorrectPair = ref(null);
const wrongAttemptCount = ref(0);

const question = computed(() => exerciseStore.currentQuestion);

const isCorrectlyMatched = (type, value) => {
  if (type === 'word') {
    return correctlyMatchedPairs.value.some(p => p.word === value);
  }
  return correctlyMatchedPairs.value.some(p => p.meaning === value);
};

const selectWord = (word) => {
  if (isCorrectlyMatched('word', word)) return;
  selectedWord.value = word;
  tryMatch();
};

const selectMeaning = (meaning) => {
  if (isCorrectlyMatched('meaning', meaning)) return;
  selectedMeaning.value = meaning;
  tryMatch();
};

const tryMatch = () => {
  if (selectedWord.value && selectedMeaning.value) {
    const isCorrect = question.value.correct_pairs[selectedWord.value] === selectedMeaning.value;

    if (isCorrect) {
      correctlyMatchedPairs.value = [
        ...correctlyMatchedPairs.value,
        {word: selectedWord.value, meaning: selectedMeaning.value}
      ];

      selectedWord.value = null;
      selectedMeaning.value = null;
    } else {
      wrongAttemptCount.value++;
      incorrectPair.value = {word: selectedWord.value, meaning: selectedMeaning.value};
      setTimeout(() => {
        incorrectPair.value = null;
        selectedWord.value = null;
        selectedMeaning.value = null;
      }, 800);
    }
  }
};

const allCorrectlyMatched = computed(() => {
  if (!question.value || !question.value.words) return false;
  return correctlyMatchedPairs.value.length === question.value.words.length;
});

const nextStep = () => {
  exerciseStore.submitAnswer({
    type: 'word_matching_round_completed',
    topic: question.value.topic,
    totalMatches: question.value.words.length,
    wrongAttempts: wrongAttemptCount.value,
  });
};

watch(() => exerciseStore.currentQuestionIndex, () => {
  selectedWord.value = null;
  selectedMeaning.value = null;
  correctlyMatchedPairs.value = [];
  incorrectPair.value = null;
  wrongAttemptCount.value = 0;
});
</script>

<template>
  <div class="exercise-wrapper">
    <div class="exercise-content">
      <div class="question-panel">
        <h2>"{{ question.topic }}" konusundaki kelimeleri eşleştir:</h2>
      </div>
      <div class="matching-area">
        <div class="column">
          <button
            v-for="word in question.words"
            :key="word"
            class="match-button"
            @click="selectWord(word)"
            :class="{
              selected: selectedWord === word,
              correct: isCorrectlyMatched('word', word),
              incorrect: incorrectPair && incorrectPair.word === word
            }"
            :disabled="isCorrectlyMatched('word', word)"
          >
            {{ word }}
          </button>
        </div>
        <div class="column">
          <button
            v-for="meaning in question.meanings"
            :key="meaning"
            class="match-button"
            @click="selectMeaning(meaning)"
            :class="{
              selected: selectedMeaning === meaning,
              correct: isCorrectlyMatched('meaning', meaning),
              incorrect: incorrectPair && incorrectPair.meaning === meaning
            }"
            :disabled="isCorrectlyMatched('meaning', meaning)"
          >
            {{ meaning }}
          </button>
        </div>
      </div>
    </div>

    <footer class="exercise-footer">
      <div class="feedback-box">
        <h3 v-if="!allCorrectlyMatched">Doğru çiftleri bul.</h3>
        <h3 v-else>Sonraki adıma geçebilirsin.</h3>
      </div>
      <button @click="nextStep" class="btn btn-primary" :disabled="!allCorrectlyMatched">
        Devam Et
      </button>
    </footer>
  </div>
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

.question-panel h2 {
  text-align: center;
  margin-bottom: 2rem;
}

.matching-area {
  display: flex;
  justify-content: space-around;
  gap: 2rem;
  margin-bottom: 2rem;
}

.column {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 40%;
}

.match-button {
  padding: 1rem;
  font-size: 1.1rem;
  border: 2px solid var(--border-color);
  border-radius: 12px;
  background: var(--surface-color);
  cursor: pointer;
  transition: all 0.2s;
}

.match-button.selected {
  border-color: var(--primary-color);
  background-color: #eaf2fd;
}

.match-button.correct {
  border-color: var(--success-color);
  background-color: #d4edda;
  color: #155724;
  cursor: default;
}

.match-button.incorrect {
  border-color: var(--danger-color);
  background-color: #f8d7da;
  color: #721c24;
  cursor: default;
  animation: shake 0.5s;
}

.match-button:disabled:not(.incorrect) {
  cursor: not-allowed;
}

@keyframes shake {
  0%, 100% {
    transform: translateX(0);
  }
  25% {
    transform: translateX(-5px);
  }
  75% {
    transform: translateX(5px);
  }
}

.exercise-footer {
  width: 100%;
  padding: 1.5rem 2rem;
  border-top: 2px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-sizing: border-box;
}

.feedback-box h3 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--text-secondary);
}
</style>
