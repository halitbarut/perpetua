import apiClient from './api';

export const userService = {
  getLeaderboard() {
    return apiClient.get('/users/leaderboard');
  },
  getAIFeedback() {
    return apiClient.get('/users/me/feedback');
  },
  /**
   * Kullanıcının mevcut dil seviyesini günceller.
   * @param {string} level - Yeni seviye (örn: "B1")
   * @returns {Promise<object>} - Güncellenmiş kullanıcı verisi.
   */
  updateUserLevel(level) {
    return apiClient.put('/users/me/level', { level });
  },
};
