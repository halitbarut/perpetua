import apiClient from './api';

export const exerciseService = {
  /**
   * Backend'den yeni bir alıştırma oturumu ister.
   * @param {string} exerciseType - 'grammar', 'dialogue', veya 'word_matching'
   * @returns {Promise<object>} - Alıştırma verilerini içeren Promise
   */
  getNewExercise(exerciseType) {
    return apiClient.get('/exercise/', {
      params: {
        exercise_type: exerciseType,
      },
    });
  },

  /**
   * Tamamlanmış bir alıştırmanın sonuçlarını değerlendirme için backend'e gönderir.
   * @param {object} payload - ExerciseResultPayload şemasına uygun nesne
   * @returns {Promise<object>} - Puan ve geri bildirim içeren Promise
   */
  evaluateExercise(payload) {
    return apiClient.post('/exercise/evaluate', payload);
  },
};
