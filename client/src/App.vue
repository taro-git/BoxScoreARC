<template>
  <div class="app">
    <router-view />
    
    <footer class="footer">
      <router-link to="/" class="nav">🏠<br>ホーム</router-link>
      <router-link to="/matches" class="nav">🏀<br>Matches</router-link>
      <router-link to="/news" class="nav">📰<br>ニュース</router-link>
      <router-link to="/video" class="nav">▶️<br>ビデオ</router-link>
      <router-link to="/data" class="nav">📊<br>データ</router-link>
    </footer>
  </div>
</template>

<script setup lang="ts">
// 特に追加コードなし
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  max-height: 100vh;
}

.footer {
  display: flex;
  justify-content: space-around;
  background-color: #0a2c64;
  padding: 10px 0;
  color: white;
  font-size: 12px;
  height: 38px;
  border-top: 1px solid #ccc;
  flex-shrink: 0; /* フッターが縮小しない */
}

.nav {
  text-align: center;
  text-decoration: none;
  color: white;
}

.nav.router-link-active {
  color: #fff;
  font-weight: bold;
}
</style>
