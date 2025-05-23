<template>
  <div>
    <h2>nba_api 応答</h2>
    <p v-if="error">エラー: {{ error }}</p>
    <p v-else-if="data">応答: {{ data }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

// eslint-disable-next-line @typescript-eslint/no-explicit-any
const data = ref<any | null>(null)
const error = ref<string | null>(null)
axios.get('http://172.16.0.62:1026/api/nbaapi-test?date=2025-05-14')
        .then(res => {
          data.value = res.data
        })
        .catch(err => {
          error.value = err.message
        })
</script>
