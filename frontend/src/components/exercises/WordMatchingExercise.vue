<!-- frontend/src/components/exercises/WordMatchingExercise.vue (NİHAİ VE TAM HALİ) -->
<script setup>
import { ref, computed, watch } from 'vue';
import { useExerciseStore } from '@/store/exercise';

const exerciseStore = useExerciseStore();

const selectedWord = ref(null);
const selectedMeaning = ref(null);
const matchedPairs = ref([]); // Yapısı: { word, meaning, isCorrect }

const question = computed(() => exerciseStore.currentQuestion);

// Bir kelimenin daha önce eşleşip eşleşmediğini kontrol eder
const isWordMatched = (word) => matchedPairs.value.some(p => p.word === word);
// Bir anlamın daha önce eşleşip eşleşmediğini kontrol eder
const isMeaningMatched = (meaning) => matchedPairs.value.some(p => p.meaning === meaning);

const selectWord = (word) => {
  if (isWordMatched(word)) return;
  selectedWord.value = word;
  tryMatch();
};

const selectMeaning = (meaning) => {
  if (isMeaningMatched(meaning)) return;
  selectedMeaning.value = meaning;
  tryMatch();
};

const tryMatch = () => {
  // Eğer hem bir kelime hem de bir anlam seçilmişse eşleştirmeyi dene
  if (selectedWord.value && selectedMeaning.value) {
    // Backend'den gelen cevap anahtarını kullanarak doğruluğu kontrol et
    const isCorrect = question.value.correct_pairs[selectedWord.value] === selectedMeaning.value;

    // Eşleşen çifti, doğruluk bilgisiyle birlikte listeye ekle
    matchedPairs.value.push({
      word: selectedWord.value,
      meaning: selectedMeaning.value,
      isCorrect: isCorrect
    });

    // Seçimleri sıfırla
    selectedWord.value = null;
    selectedMeaning.value = null;
  }
};

// Tüm kelimelerin eşleşip eşleşmediğini kontrol eden computed property
const allMatched = computed(() => {
  if (!question.value || !question.value.words) return false;
  return matchedPairs.value.length === question.value.words.length;
});

const nextStep = () => {
  // Backend'e göndereceğimiz cevap, kullanıcının yaptığı tüm eşleştirmelerdir.
  exerciseStore.submitAnswer({
    type: 'word_matching_round_completed',
    topic: question.value.topic,
    user_pairs: matchedPairs.value,
  });
};

// Bir sonraki soruya geçildiğinde tüm yerel state'i sıfırla
watch(() => exerciseStore.currentQuestionIndex, () => {
  selectedWord.value = null;
  selectedMeaning.value = null;
  matchedPairs.value = [];
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
              correct: isWordMatched(word) && matchedPairs.find(p => p.word === word).isCorrect,
              incorrect: isWordMatched(word) && !matchedPairs.find(p => p.word === word).isCorrect
            }"
            :disabled="isWordMatched(word)"
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
              correct: isMeaningMatched(meaning) && matchedPairs.find(p => p.meaning === meaning).isCorrect,
              incorrect: isMeaningMatched(meaning) && !matchedPairs.find(p => p.meaning === meaning).isCorrect
            }"
            :disabled="isMeaningMatched(meaning)"
          >
            {{ meaning }}
          </button>
        </div>
      </div>
    </div>

    <footer class="exercise-footer">
      <div class="feedback-box">
        <h3 v-if="!allMatched">Eşleştirmek için bir kelime ve bir anlam seç.</h3>
        <h3 v-else>Harika! Tüm kelimeler eşleşti.</h3>
      </div>
      <button @click="nextStep" class="btn btn-primary" :disabled="!allMatched">
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
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}
.exercise-footer {
  width: 100%;
  padding: 1.5rem 0;
  border-top: 2px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.feedback-box h3 {
  margin: 0;
  font-size: 1.2rem;
  color: var(--text-secondary);
}
</style>
