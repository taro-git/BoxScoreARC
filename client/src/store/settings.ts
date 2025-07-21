import { type quarterRangeVariations } from '../types/QuarterRangeVariations'
import { defineStore } from 'pinia'
import { DEFAULT_THEME_COLOR_BASE } from '../vuetify'
import { type RgbaColor } from '../core/colorControl'


interface SettingsState {
    scoreDisplay: boolean
    defaultQuarterRangeType: quarterRangeVariations
    themeColor: RgbaColor
}

export const settingsStore = defineStore('settings', {
    state: (): SettingsState => ({
        scoreDisplay: true,
        defaultQuarterRangeType: 'fourQuarters',
        themeColor: DEFAULT_THEME_COLOR_BASE
    }),
    persist: true,
})