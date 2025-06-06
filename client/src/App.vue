<template>
    <div class="app">
        <router-view />

        <footer class="footer">
            <router-link to="/" class="nav">🏠<br>Home</router-link>
            <router-link to="/games" class="nav">🏀<br>Games</router-link>
            <router-link to="/analysys" class="nav">📰<br>Analysys</router-link>
            <router-link to="/data" class="nav">📊<br>Data</router-link>
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
    height: 100vh;
}

.footer {
    display: flex;
    justify-content: space-around;
    background-color: var(--footer-backgroud-color);
    padding: 10px 0;
    font-size: 12px;
    height: var(--footer-height);
    border-top: var(--border);
    box-sizing: border-box;
    flex-shrink: 0;
    /* フッターが縮小しない */
}

.nav {
    color: #fff;
    text-decoration: none;
    text-align: center;
}
</style>
