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
      let correctRounds = 0;
      const finalWrongAnswers = [];

      this.questions.forEach((question, index) => {
        const userAnswerData = this.userAnswers[index];
        let isRoundCorrect = false;

        switch (question.type) {
          case 'grammar':
          case 'dialogue':
            { const correctAnswer = question.type === 'grammar' ? question.correct_word : question.correct_answer;
            const questionText = question.type === 'grammar' ? question.sentence_template : question.question;
            isRoundCorrect = userAnswerData === correctAnswer;
            if (!isRoundCorrect) {
              finalWrongAnswers.push({
                question: questionText,
                user_answer: userAnswerData,
                correct_answer: correctAnswer,
              });
            }
            break; }

          case 'word_matching':
            { const correctMatchesInRound = userAnswerData.correct_pairs;
            const totalMatchesInRound = userAnswerData.total_pairs;
            isRoundCorrect = correctMatchesInRound === totalMatchesInRound;
            if (!isRoundCorrect) {
              finalWrongAnswers.push({
                question: `Kelime Eşleştirme (${question.topic})`,
                user_answer: `${correctMatchesInRound}/${totalMatchesInRound} doğru yaptın.`,
                correct_answer: `Tüm kelimeleri doğru eşleştirmelisin.`
              });
            }
            break; }
        }

        if (isRoundCorrect) {
          correctRounds++;
        }
      });

      const totalRounds = this.questions.length;
      const finalScore = totalRounds > 0 ? Math.round((correctRounds / totalRounds) * 100) : 0;

      return {
        total_questions: totalRounds,
        correct_answers: correctRounds,
        wrong_answers: finalWrongAnswers,
        final_score: finalScore, // <-- HESAPLANAN PUANI PAYLOAD'A EKLE
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
