<template>
    <div class="error-wrapper">
        <div class="server-error">Server Error !!</div>
        <div class="error-message">{{ errorMessage }}</div>
    </div>
</template>

<script setup lang="ts">
import { defineProps } from 'vue'

defineProps<{
    errorMessage: string
}>()

</script>

<style scoped>
.error-wrapper {
    margin-top: 10px;
    color: var(--error-font-color);
    background-color: var(--error-backgroud-color);
    border: var(--error-border);
    border-radius: 6px;

}

.server-error {
    font-size: 30px;
    font-weight: bold;
    text-align: center;
}

.error-message {
    padding: 12px 16px;
    font-size: 14px;
    font-family: sans-serif;

    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: pre-wrap;

    max-width: 100%;
    box-sizing: border-box;
}

.error-message::before {
    content: "⚠ ";
    font-weight: bold;
}
</style>
