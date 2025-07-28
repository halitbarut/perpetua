<script setup>
import { ref, onMounted } from 'vue';
import { userService } from '@/services/user.service';
import { useRouter } from 'vue-router';

const leaderboard = ref([]);
const isLoading = ref(true);
const error = ref(null);
const router = useRouter();

onMounted(async () => {
  try {
    const { data } = await userService.getLeaderboard();
    leaderboard.value = data;
  } catch (err) {
    error.value = 'Liderlik tablosu yüklenirken bir hata oluştu.';
    console.error(err);
  } finally {
    isLoading.value = false;
  }
});
</script>

<template>
  <div class="leaderboard-container">
    <div class="header">
      <button @click="router.push('/dashboard')" class="back-btn">‹ Geri</button>
      <h1>🏆 Liderlik Tablosu</h1>
    </div>

    <div v-if="isLoading" class="loading">Yükleniyor...</div>
    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="!isLoading && !error" class="leaderboard-list">
      <table>
        <thead>
        <tr>
          <th>Sıra</th>
          <th>Kullanıcı</th>
          <th>Puan</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="(user, index) in leaderboard" :key="user.id">
          <td class="rank">
            <span v-if="index < 3" class="medal">{{ ['🥇', '🥈', '🥉'][index] }}</span>
            <span v-else>{{ index + 1 }}</span>
          </td>
          <td class="username">{{ user.username }}</td>
          <td class="score">{{ user.weekly_score }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.leaderboard-container { max-width: 700px; margin: 2rem auto; padding: 2rem; background-color: var(--surface-color); border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.1); }
.header { display: flex; align-items: center; gap: 1rem; margin-bottom: 2rem; }
.back-btn { background: none; border: none; font-size: 2rem; cursor: pointer; color: var(--text-secondary); padding: 0.5rem; line-height: 1; }
table { width: 100%; border-collapse: collapse; }
th, td { padding: 1rem; text-align: left; }
thead th { border-bottom: 2px solid var(--border-color); color: var(--text-secondary); font-weight: 600; }
tbody tr:not(:last-child) { border-bottom: 1px solid var(--border-color); }
.rank { font-size: 1.5rem; font-weight: bold; text-align: center; width: 100px; color: var(--text-secondary); }
.medal { font-size: 2rem; }
.username { font-weight: 500; }
.score { font-weight: 700; color: var(--primary-color); text-align: right; }
</style>
