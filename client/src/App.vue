<template>
    <div class="app">
        <router-view />

        <footer class="footer">
            <router-link to="/" class="nav">🏠<br>Home</router-link>
            <router-link to="/games" class="nav">🏀<br>Games</router-link>
            <router-link to="/analysis" class="nav">📊<br>Analysis</router-link>
            <router-link to="/settings" class="nav">⚙️<br>Settings</router-link>
        </footer>
    </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'

function setViewportHeight(): void {
    const vh = window.innerHeight * 0.01
    document.documentElement.style.setProperty('--vh', `${vh}px`)
}

onMounted(() => {
    setViewportHeight()
    window.addEventListener('resize', setViewportHeight)
    window.addEventListener('orientationchange', setViewportHeight)
})

onBeforeUnmount(() => {
    window.removeEventListener('resize', setViewportHeight)
    window.removeEventListener('orientationchange', setViewportHeight)
})
</script>

<style scoped>
.app {
    display: flex;
    flex-direction: column;
    height: calc(var(--vh, 1vh) * 100);
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
