<template>
  <div class="container">test: {{ gameId }}</div>
</template>

<script setup lang="ts">
  import { defineProps } from 'vue'

  defineProps<{
    gameId: string
  }>()

</script>


<style scoped>

.container {
  background-color: var(--main-backgroud-color);
  color: #fff;
  height: calc(100% - var(--footer-height));
  display: flex;
  flex-direction: column;
}

</style>
