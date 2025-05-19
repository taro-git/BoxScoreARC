import { Ref, ref } from 'vue'

import type { MatchSummary } from '@/types/MatchSummary'

export class MatchSummariesSets {
  numberOfPreviousDays: number
  numberOfFutureDays: number
  dayOffsetsList: number[]
  matchSummaryMap: Ref<{ [key: number]: MatchSummary[]}>
  isLoadingMap: Ref<{ [key: number]: boolean }>
  error: Ref<{ [key: number]: { isError: boolean, errorMessage: string } }>

  constructor(numberOfPreviousDays: number, numberOfFutureDays: number) {
    this.numberOfPreviousDays = numberOfPreviousDays
    this.numberOfFutureDays = numberOfFutureDays
    this.dayOffsetsList = Array.from({ length: this.numberOfFutureDays + this.numberOfPreviousDays + 1 }, (_, i) => i - this.numberOfPreviousDays)
    this.matchSummaryMap = ref({})
    this.isLoadingMap = ref({})
    this.error = ref({})

    for (let i = -numberOfPreviousDays; i <= numberOfFutureDays; i++) {
      this.matchSummaryMap.value[i] = []
      this.isLoadingMap.value[i] = true
      this.error.value[i] = {
        isError: false,
        errorMessage: ''
      }
    }
  }
}