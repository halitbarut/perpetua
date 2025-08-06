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
    }, isSessionFinished: (state) => {
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
      let totalCorrectItems = 0;
      let totalPossibleItems = 0;
      const finalWrongAnswers = [];

      this.questions.forEach((question, index) => {
        const userAnswerData = this.userAnswers[index];

        if (question.type === 'grammar' || question.type === 'dialogue') {
          totalPossibleItems += 1;
          const correctAnswer = question.type === 'grammar' ? question.correct_word : question.correct_answer;
          if (userAnswerData === correctAnswer) {
            totalCorrectItems += 1;
          } else {
            const questionText = question.type === 'grammar' ? question.sentence_template : question.question;
            finalWrongAnswers.push({
              question: questionText,
              user_answer: userAnswerData,
              correct_answer: correctAnswer,
            });
          }
        } else if (question.type === 'word_matching') {
          const totalPairs = userAnswerData.totalPairs;
          const wrongAttempts = userAnswerData.wrongAttempts;

          // Bu turdaki toplam olası doğru sayısı
          totalPossibleItems += totalPairs;

          // Net doğru sayısı = Toplam - Yanlış denemeler (0'dan az olamaz)
          const netCorrect = Math.max(0, totalPairs - wrongAttempts);
          totalCorrectItems += netCorrect;

          if (wrongAttempts > 0) {
            finalWrongAnswers.push({
              question: `Kelime Eşleştirme (${question.topic})`,
              user_answer: `${netCorrect}/${totalPairs} doğru`,
              correct_answer: `Bu turda ${wrongAttempts} yanlış deneme yaptın.`
            });
          }
        }
      });

      const finalScore = totalPossibleItems > 0 ? Math.round((totalCorrectItems / totalPossibleItems) * 100) : 0;

      return {
        total_questions: totalPossibleItems,
        correct_answers: totalCorrectItems,
        wrong_answers: finalWrongAnswers,
        final_score: finalScore,
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
