import {defineStore} from 'pinia';
import {exerciseService} from '@/services/exercise.service';
import {useAuthStore} from './auth';

export const useExerciseStore = defineStore('exercise', {
  state: () => ({
    questions: [],
    currentQuestionIndex: 0,
    userAnswers: [],
    isSessionActive: false,
    isLoading: false,
    error: null,
    finalScore: null,
    finalFeedback: null,
  }),

  getters: {
    currentQuestion: (state) => {
      if (state.isSessionActive && state.questions.length > 0) {
        return state.questions[state.currentQuestionIndex];
      }
      return null;
    },
    isSessionFinished: (state) => {
      return state.isSessionActive && state.currentQuestionIndex >= state.questions.length;
    },
  },

  actions: {
    async startNewSession(exerciseType) {
      this.isLoading = true;
      this.error = null;
      this.resetSession();

      try {
        const {data} = await exerciseService.getNewExercise(exerciseType);
        this.questions = data.questions;
        this.isSessionActive = true;
      } catch (err) {
        this.error = 'Alıştırma yüklenirken bir hata oluştu.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    submitAnswer(answer) {
      if (!this.isSessionActive) return;

      this.userAnswers.push(answer);
      this.currentQuestionIndex++;

      if (this.isSessionFinished) {
        this.evaluateSession();
      }
    },

    async evaluateSession() {
      const authStore = useAuthStore();
      this.isLoading = true;
      const payload = this.prepareEvaluationPayload();

      try {
        const {data} = await exerciseService.evaluateExercise(payload);
        this.finalScore = data.score;
        this.finalFeedback = data.feedback;
        await authStore.fetchCurrentUser();
      } catch (err) {
        this.error = 'Sonuçlar değerlendirilirken bir hata oluştu.';
        console.error(err);
      } finally {
        this.isLoading = false;
      }
    },

    prepareEvaluationPayload() {
      let correctCount = 0;
      const wrongAnswers = [];

      this.questions.forEach((question, index) => {
        const userAnswer = this.userAnswers[index]; // Bu artık bir obje
        let isCorrect = false;

        switch (question.type) {
          case 'grammar':
          case 'dialogue':
            const correctAnswer = question.type === 'grammar' ? question.correct_word : question.correct_answer;
            const questionText = question.type === 'grammar' ? question.sentence_template : question.question;
            isCorrect = userAnswer === correctAnswer;
            if (!isCorrect) {
              wrongAnswers.push({ question: questionText, user_answer: userAnswer, correct_answer: correctAnswer });
            }
            break;

          case 'word_matching':
            // userAnswer: { type: '...', topic: '...', user_pairs: [...] }
            // user_pairs'daki her bir eşleşmenin doğruluğunu sayalım
            const correctMatchesInRound = userAnswer.user_pairs.filter(p => p.isCorrect).length;
            const totalMatchesInRound = question.words.length;

            // Turu başarılı saymak için basit bir kural: yarıdan fazlası doğruysa
            if (correctMatchesInRound > totalMatchesInRound / 2) {
              isCorrect = true;
            }

            // Yanlışları wrongAnswers'a ekleyelim
            userAnswer.user_pairs.filter(p => !p.isCorrect).forEach(wrongPair => {
              wrongAnswers.push({
                question: `Eşleştirme (${question.topic}): ${wrongPair.word}`,
                user_answer: wrongPair.meaning,
                correct_answer: question.correct_pairs[wrongPair.word],
              });
            });
            break;
        }

        if (isCorrect) {
          correctCount++;
        }
      });

      return {
        total_questions: this.questions.length, // 5 tur
        correct_answers: correctCount,
        wrong_answers: wrongAnswers,
      };
    },

    resetSession() {
      this.questions = [];
      this.currentQuestionIndex = 0;
      this.userAnswers = [];
      this.isSessionActive = false;
      this.finalScore = null;
      this.finalFeedback = null;
      this.error = null;
    },
  },
});
