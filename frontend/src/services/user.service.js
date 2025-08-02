import apiClient from './api';

export const userService = {
  getLeaderboard() {
    return apiClient.get('/users/leaderboard');
  },

  /**
   * Kullanıcının son hatalarına göre kişisel bir AI tavsiyesi alır.
   * @returns {Promise<string>} - AI tarafından üretilen tavsiye metni.
   */
  getAIFeedback() {
    return apiClient.get('/users/me/feedback'); // YENİ FONKSİYON
  },
};
