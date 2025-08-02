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
      let totalAttempts = 0; // Toplam deneme (hamle) sayısı
      let totalCorrectMoves = 0; // Toplam doğru hamle sayısı
      const finalWrongAnswers = []; // AI'a gönderilecek spesifik hatalar

      this.questions.forEach((question, index) => {
        const userAnswerData = this.userAnswers[index];

        switch (question.type) {
          case 'grammar':
          case 'dialogue':
            { totalAttempts += 1; // Her tur tek bir denemedir
            const correctAnswer = question.type === 'grammar' ? question.correct_word : question.correct_answer;
            const isCorrect = userAnswerData === correctAnswer;
            if (isCorrect) {
              totalCorrectMoves++;
            } else {
              const questionText = question.type === 'grammar' ? question.sentence_template : question.question;
              finalWrongAnswers.push({
                question: questionText,
                user_answer: userAnswerData,
                correct_answer: correctAnswer,
              });
            }
            break; }

          case 'word_matching':
            { const correctMovesInRound = userAnswerData.totalMatches;
            const wrongMovesInRound = userAnswerData.wrongAttempts;
            const totalMovesInRound = correctMovesInRound + wrongMovesInRound;

            totalCorrectMoves += correctMovesInRound;
            totalAttempts += totalMovesInRound;

            if (wrongMovesInRound > 0) {
              finalWrongAnswers.push({
                question: `Kelime Eşleştirme Turu (${question.topic})`,
                user_answer: `Bu turda ${wrongMovesInRound} yanlış deneme yaptın.`,
                correct_answer: `Tüm kelimeleri ilk denemede doğru eşleştirmeye çalışmalısın.`
              });
            }
            break; }
        }
      });

      const finalScore = totalAttempts > 0 ? Math.round((totalCorrectMoves / totalAttempts) * 100) : 0;

      return {
        total_questions: totalAttempts,
        correct_answers: totalCorrectMoves,
        final_score: finalScore,
        wrong_answers: finalWrongAnswers,
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
