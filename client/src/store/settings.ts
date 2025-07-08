import { quarterRangeVariations } from '@/types/quarterRangeVariations'
import { defineStore } from 'pinia'

interface SettingsState {
    scoreDisplay: boolean
    defaultQuarterRangeType: quarterRangeVariations
}

export const settingsStore = defineStore('settings', {
    state: (): SettingsState => ({
        scoreDisplay: true,
        defaultQuarterRangeType: 'fourQuarters',
    }),
    persist: true,
})