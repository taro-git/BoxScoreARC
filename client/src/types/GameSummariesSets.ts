import { Ref, ref } from 'vue'

import type { GameSummary } from '@/types/GameSummary'

export class GameSummariesSets {
    numberOfPreviousDays: number
    numberOfFutureDays: number
    dayOffsetsList: number[]
    gameSummaryMap: Ref<{ [key: number]: GameSummary[] }>
    isLoadingMap: Ref<{ [key: number]: boolean }>
    error: Ref<{ [key: number]: { isError: boolean, errorMessage: string } }>

    constructor(numberOfPreviousDays: number, numberOfFutureDays: number) {
        this.numberOfPreviousDays = numberOfPreviousDays
        this.numberOfFutureDays = numberOfFutureDays
        this.dayOffsetsList = Array.from({ length: this.numberOfFutureDays + this.numberOfPreviousDays + 1 }, (_, i) => i - this.numberOfPreviousDays)
        this.gameSummaryMap = ref({})
        this.isLoadingMap = ref({})
        this.error = ref({})

        for (let i = -numberOfPreviousDays; i <= numberOfFutureDays; i++) {
            this.gameSummaryMap.value[i] = []
            this.isLoadingMap.value[i] = true
            this.error.value[i] = {
                isError: false,
                errorMessage: ''
            }
        }
    }
}