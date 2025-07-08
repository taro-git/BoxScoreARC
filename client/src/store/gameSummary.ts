import { defineStore } from 'pinia'

import { GameSummary } from '@/types/GameSummary'


export const gameSummaryStore = defineStore('gameSummary', {
    state: (): GameSummary => ({
        game_id: '',
        home_team: '',
        home_logo: '',
        away_team: '',
        away_logo: '',
        status_text: '',
        status_id: 0,
        live_period: 0,
        live_clock: '',
        game_category: '',
    }),
    actions: {
        setStatusText(statusText: string) {
            this.status_text = statusText
        }
    }
})