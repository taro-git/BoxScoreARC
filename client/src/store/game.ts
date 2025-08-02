import { defineStore } from 'pinia'

import { GameSummary } from '../types/GameSummary'

interface GameState {
    gameSummary: GameSummary
    finalPeriod: number
}

export const gameStore = defineStore('game', {
    state: (): GameState => ({
        gameSummary: new GameSummary(),
        finalPeriod: 4
    }),
    actions: {
        setStatusText(statusText: string) {
            this.gameSummary.statusText = statusText
        }
    }
})