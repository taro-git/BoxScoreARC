<template>
    <div class="container">
        <header class="settings-header">
            Settings
        </header>
        <table class="settings-table">
            <tr>
                <th>
                    display score
                </th>
                <td>
                    <ToggleSwitch v-model="settings.scoreDisplay" :size="60" />
                </td>
            </tr>
        </table>
    </div>
</template>

<script setup lang="ts">
import ToggleSwitch from '@/components/ToggleSwitch.vue'
import { settingsStore } from '@/store/settings'

const settings = settingsStore()


</script>

<style scoped>
.container {
    background-color: var(--main-backgroud-color);
    color: #fff;
    height: calc(100% - var(--footer-height));
    display: flex;
    flex-direction: column;
    font-size: large;
    overflow-y: auto;
}

.settings-header {
    padding: 12px 0px;
    font-size: 20px;
    width: 100%;
    text-align: center;
}

.settings-table {
    width: 100%;
    padding: 0px 20px 0px 20px;
    border-spacing: 0px;
    background-color: var(--dark-backgroud-color);
    position: relative;
}

.settings-table::-webkit-scrollbar {
    display: none;
}

.settings-table th {
    border-top: 1px solid rgba(128, 128, 128, 0.5);
    border-bottom: 1px solid rgba(128, 128, 128, 0.5);
    text-align: left;
    align-items: center;
    padding: 8px;
    height: 40px;
}

.settings-table td {
    border-top: 1px solid rgba(128, 128, 128, 0.5);
    border-bottom: 1px solid rgba(128, 128, 128, 0.5);
    display: flex;
    justify-content: flex-end;
    align-items: center;
    padding: 8px;
    height: 40px
}
</style>
