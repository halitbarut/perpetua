<script setup>
import { ref, onMounted } from 'vue';
defineProps({
  title: { type: String, default: 'Yükleniyor...' }
});

const tips = [
  "Bir kelimeyi günde 7 farklı zamanda görmek, onu kalıcı hafızaya almayı kolaylaştırır.",
  "Yanlış yapmaktan korkma! Her hata, öğrenme sürecinin bir parçasıdır.",
  "Yeni bir dil öğrenmek, beyninde yeni sinirsel yollar oluşturur.",
  "Her gün sadece 15 dakika pratik yapmak, hiç yapmamaktan çok daha etkilidir.",
  "Dinleme pratiği için sevdiğin yabancı şarkıları sözleriyle takip etmeyi dene.",
  "Öğrendiğin yeni bir kelimeyi gün içinde 3 farklı cümlede kullanmaya çalış.",
  "Dil öğrenirken yapılan en büyük hata, konuşmaktan çekinmektir.",
  "Bir dili öğrenmenin en hızlı yolu, o dili hayatının bir parçası yapmaktır.",
  "Hedeflerini küçük ve ulaşılabilir parçalara böl: 'Bugün 5 yeni kelime öğreneceğim.' gibi.",
  "Biraz ilerledikten sonra telefonunun dilini öğrenmekte olduğun dile çevir."
];
const randomTip = ref('');
onMounted(() => {
  randomTip.value = tips[Math.floor(Math.random() * tips.length)];
});
</script>
<template>
  <div class="loading-overlay">
    <div class="loading-content">
      <div class="spinner"></div>
      <h3>{{ title }}</h3>
      <p class="tip">{{ randomTip }}</p>
    </div>
  </div>
</template>
<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.loading-content {
  text-align: center;
  color: #333;
}
.spinner {
  width: 50px;
  height: 50px;
  border: 5px solid #f3f3f3;
  border-top: 5px solid #5c6ac4;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
h3 {
  font-size: 1.5rem;
  margin-bottom: 10px;
}
.tip {
  font-size: 1rem;
  color: #555;
  max-width: 400px;
}
</style>
