<template>
    <v-sheet class="bg-base hide-scroll d-flex flex-column fill-height" fluid>
        <v-tabs v-model="selectedTab" bg-color="darken" color="accent" mandatory fixed-tabs>
            <v-tab v-for="tab in tabs" :key="tab" :value="tab">{{ tabTitles[tab] }}</v-tab>
        </v-tabs>
        <v-tabs-window v-model="selectedTab" class="fill-height">
            <v-tabs-window-item v-for="tab in tabs" :key="tab" :value="tab" class="fill-height">
                <v-sheet v-if="tab === 'boxScore' || tab === 'teamStats'" class="bg-base px-6 text-center">
                    <v-select v-model="selectedQuarterRange" label="range of quarter" :items="quarterRangeLabels" />
                    {{ formatReminTime(gameClockRange[0]) }} ~ {{ formatReminTime(gameClockRange[1]) }}
                    <v-range-slider v-model="gameClockRange" :min="minSeconds" :max="maxSeconds" color="accent"
                        class="mx-6" />
                </v-sheet>
                <component :is="tabComponents[tab]" v-bind="tabProps[tab]" />
            </v-tabs-window-item>
        </v-tabs-window>
    </v-sheet>
</template>

<script setup lang="ts">
import { ref, computed, defineProps, watch, type Component } from 'vue'

import TeamStats from '../components/TeamStats.vue'
import BoxScore from '../components/BoxScore.vue'
import HeadToHeadRecord from '../components/HeadToHeadRecord.vue'
import { gameSummaryStore } from '../store/gameSummary'
import { settingsStore } from '../store/settings'
import { type quarterRangeVariations, quarterRangeLabels } from '../types/QuarterRangeVariations'

const props = defineProps<{
    gameId: string
}>()

const tabs = ['teamStats', 'boxScore', 'headToHeadRecord'] as const
type TabKey = typeof tabs[number]
const selectedTab = ref<TabKey>('boxScore')
const tabTitles: Record<TabKey, string> = {
    teamStats: 'Team Stats',
    boxScore: 'Box Score',
    headToHeadRecord: 'Head to Head Record'
}
const tabComponents: Record<TabKey, Component> = {
    teamStats: TeamStats,
    boxScore: BoxScore,
    headToHeadRecord: HeadToHeadRecord
}
const tabProps = computed<Record<TabKey, Object>>(() => ({
    teamStats: {},
    boxScore: {
        gameId: props.gameId,
        gameClockRange: gameClockRange
    },
    headToHeadRecord: {}
}))

const selectedQuarterRange = ref<quarterRangeVariations>(settingsStore().defaultQuarterRangeType)
const gameSummary = gameSummaryStore()
const endQuater = gameSummary.live_period
const quaterRange: Record<quarterRangeVariations, Record<'maxQuater' | 'minQuater', number>> = {
    Q1: { maxQuater: 1, minQuater: 1 },
    Q2: { maxQuater: 2, minQuater: 2 },
    firstHalf: { maxQuater: 2, minQuater: 1 },
    Q3: { maxQuater: 3, minQuater: 3 },
    Q4: { maxQuater: 4, minQuater: 4 },
    secondHalf: { maxQuater: 4, minQuater: 3 },
    fourQuarters: { maxQuater: 4, minQuater: 1 },
    all: { maxQuater: endQuater, minQuater: 1 },
    OT: { maxQuater: endQuater <= 4 ? 5 : endQuater, minQuater: 5 }
}
const maxSeconds = computed(() => {
    const maxQuarter = quaterRange[selectedQuarterRange.value].maxQuater
    return maxQuarter <= 4 ? 12 * maxQuarter * 60 : endQuater == 4 ? 12 * 4 * 60 : 12 * 4 * 60 + 5 * (maxQuarter - 4) * 60
})
const minSeconds = computed(() => {
    const minQuarter = quaterRange[selectedQuarterRange.value].minQuater
    return minQuarter <= 4 ? 12 * (minQuarter - 1) * 60 : 12 * 4 * 60 + 5 * (minQuarter - 5) * 60
})
const gameClockRange = ref([minSeconds.value, minSeconds.value])
watch(selectedQuarterRange, () => {
    const min = minSeconds.value
    const max = maxSeconds.value
    const [start, end] = gameClockRange.value

    const clampedStart = Math.max(min, Math.min(start, max))
    const clampedEnd = Math.max(min, Math.min(end, max))

    gameClockRange.value = [clampedStart, clampedEnd]
})

const formatReminTime = (seconds: number) => {
    let nth = ''
    let reminMinutes = 12
    let reminSeconds = 0
    let reminTime = ''
    if (seconds < 48 * 60) {
        let quarter = 0
        if (seconds % (12 * 60) !== 0) {
            quarter = Math.floor((seconds) / (12 * 60)) + 1
        } else {
            if (seconds === minSeconds.value) {
                quarter = quaterRange[selectedQuarterRange.value].minQuater
            } else {
                quarter = Math.floor((seconds) / (12 * 60))
            }
        }
        switch (quarter) {
            case 1:
                nth = '1st Q.'
                break
            case 2:
                nth = '2nd Q.'
                break
            case 3:
                nth = '3rd Q.'
                break
            case 4:
                nth = '4th Q.'
                break
        }
        reminSeconds = quarter * 12 * 60 - seconds
        reminMinutes = Math.floor(reminSeconds / 60)
        reminSeconds = reminSeconds % 60
    } else if (seconds === 48 * 60) {
        if (seconds === minSeconds.value) {
            nth = 'OT1'
            reminMinutes = 5
            reminSeconds = 0
        } else {
            nth = '4th Q.'
            reminMinutes = 0
            reminSeconds = 0
        }
    } else {
        const otSeconds = seconds - 48 * 60
        let ot = 0
        if (otSeconds % (5 * 60) !== 0) {
            ot = Math.floor(otSeconds / (5 * 60)) + 1
        } else {
            ot = Math.floor(otSeconds / (5 * 60))
        }
        nth = `OT${ot}`
        reminSeconds = ot * 5 * 60 - otSeconds
        reminMinutes = Math.floor(reminSeconds / 60)
        reminSeconds = reminSeconds % 60
    }
    if (reminMinutes === 0) {
        const roundedReminSeconds = reminSeconds.toFixed(1)
        reminTime = `${roundedReminSeconds} s`
    } else {
        reminSeconds = Math.floor(reminSeconds)
        const paddedReminMinutes = String(reminMinutes).padStart(2, '0')
        const paddedReminSeconds = String(reminSeconds).padStart(2, '0')
        reminTime = `${paddedReminMinutes}:${paddedReminSeconds}`
    }
    return `${nth} ${reminTime}`
}

</script>


<style scoped></style>
