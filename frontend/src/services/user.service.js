import apiClient from './api';

export const userService = {
  /**
   * Liderlik tablosu verisini çeker.
   * @returns {Promise<Array>} - Puanlarına göre sıralanmış kullanıcı listesi.
   */
  getLeaderboard() {
    return apiClient.get('/users/leaderboard');
  },
};
