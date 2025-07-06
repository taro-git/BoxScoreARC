import { defineStore } from 'pinia'


export const settingsStore = defineStore('settings', {
    state: () => ({
        scoreDisplay: true,
    }),
    persist: true,
})