<template>
  <div>
    <h2>ClickHouse API 応答</h2>
    <p v-if="error">エラー: {{ error }}</p>
    <p v-else-if="data">サーバ時刻: {{ data.clickhouse_time }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const data = ref<{ clickhouse_time: string } | null>(null)
const error = ref<string | null>(null)
axios.get('http://172.16.0.62:1026/api/clickhouse-test/')
        .then(res => {
          data.value = res.data
        })
        .catch(err => {
          error.value = err.message
        })
</script>
