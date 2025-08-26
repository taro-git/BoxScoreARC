import { defineStore } from 'pinia'

import { BoxScoreColumnKeys } from '../types/BoxScore'
import { GameSummary } from '../types/GameSummary'
import { type TeamStats } from '../types/TeamStats'

interface GameState {
    gameSummary: GameSummary
    finalPeriod: number
    teamStats: TeamStats[]
}

export const gameStore = defineStore('game', {
    state: (): GameState => ({
        gameSummary: new GameSummary(),
        finalPeriod: 4,
        teamStats: BoxScoreColumnKeys.slice(2).map(key => { return { boxScoreColumnKey: key, home: 0, away: 0 } })
    }),
    actions: {
        setStatusText(statusText: string) {
            this.gameSummary.statusText = statusText
        }
    }
})