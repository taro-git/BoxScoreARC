<template>
    <div class="container">
        <GameCard v-if="!isLoading" :game-summary="gameSummary" :game-date="gameDate" :score-display="true"
            :full-view="false" />
        <div class="tab-menu">
            <div @click="activeTab = 'teamstats'" :class="['tab', activeTab === 'teamstats' ? 'selected' : '']">Team
                Stats</div>
            <div @click="activeTab = 'boxscore'" :class="['tab', activeTab === 'boxscore' ? 'selected' : '']">Box Score
            </div>
            <div @click="activeTab = 'headtoheadrecord'"
                :class="['tab', activeTab === 'headtoheadrecord' ? 'selected' : '']">Head to Head Record</div>
        </div>
        <div v-if="activeTab === 'teamstats' || activeTab === 'boxscore'" class="game-clock">
            <select v-model="selectedQuarterRange">
                <option v-for="quarterRangeLabel in quarterRangeLabels" :key="quarterRangeLabel.value"
                    :value="quarterRangeLabel.value">
                    {{ quarterRangeLabel.label }}
                </option>
            </select>
            <label for="game-time">
                {{ formatReminTime(gameClockRange[0]) }} ~ {{ formatReminTime(gameClockRange[1]) }}
            </label>
            <vue-slider class="game-clock-slider" v-model="gameClockRange" :min="minSeconds" :max="maxSeconds"
                :tooltip="'none'" :height="10" />
        </div>
        <component v-if="!isLoading" :is="currentTabComponent" v-bind="currentTabProps" />
    </div>
</template>

<script setup lang="ts">
import VueSlider from 'vue-slider-component'
import 'vue-slider-component/theme/default.css'

import { ref, computed, defineProps, watch } from 'vue'

import TeamStats from '@/components/TeamStats.vue'
import BoxScore from '@/components/BoxScore.vue'
import HeadToHeadRecord from '@/components/HeadToHeadRecord.vue'
import GameCard from '@/components/GameCard.vue'

import { CacheService } from '@/services/cacheService'
import { getBoxScoreSummary, isBoxScoreSummary, getBoxScoreRawData, isBoxScoreRawData } from '@/services/getBoxScoreService'

import { gameSummaryStore } from '@/store/gameSummary'
import { settingsStore } from '@/store/settings'

import { BoxScoreSummary } from '@/types/BoxScoreSummary'
import { BOX_SCORE_COLUMNS, BoxScoreData, BoxScoreRawData } from '@/types/BoxScore'
import { quarterRangeVariations, quarterRangeLabels } from '@/types/QuarterRangeVariations'

const props = defineProps<{
    gameId: string
    gameDate: string
}>()

const gameSummary = ref(gameSummaryStore())
gameSummary.value.away_score = 0
gameSummary.value.home_score = 0

const activeTab = ref<'teamstats' | 'boxscore' | 'headtoheadrecord'>('boxscore')

const currentTabComponent = computed(() => {
    switch (activeTab.value) {
        case 'teamstats': return TeamStats
        case 'headtoheadrecord': return HeadToHeadRecord
        default: return BoxScore
    }
})

const currentTabProps = computed(() => {
    switch (activeTab.value) {
        case 'teamstats': return {}
        case 'headtoheadrecord': return {}
        default: return {
            boxScoreSummary: boxScoreSummary.value,
            boxScoreData: boxScoreData,
        }
    }
})

const selectedQuarterRange = ref<quarterRangeVariations>(settingsStore().defaultQuarterRangeType)
const endQuater = gameSummary.value.live_period
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
    return endQuater == 4 ? 12 * 4 * 60 : maxQuarter <= 4 ? 12 * maxQuarter * 60 : 12 * 4 * 60 + 5 * (maxQuarter - 4) * 60
})
const minSeconds = computed(() => {
    const minQuarter = quaterRange[selectedQuarterRange.value].minQuater
    return minQuarter <= 4 ? 12 * (minQuarter - 1) * 60 : 12 * 4 * 60 + 5 * (minQuarter - 5) * 60
})
const gameClockRange = ref([minSeconds.value, minSeconds.value])
watch(gameClockRange, ([start_range, end_range]) => {
    updateBoxScoreData(start_range, end_range)
    gameSummary.value.away_score = boxScoreSummary.value.away.players.filter(player => !player.is_inactive).map(player => player.player_id)
        .reduce((total_pts, player_id) => total_pts + boxScoreData.value[player_id][1], 0)
    gameSummary.value.home_score = boxScoreSummary.value.home.players.filter(player => !player.is_inactive).map(player => player.player_id)
        .reduce((total_pts, player_id) => total_pts + boxScoreData.value[player_id][1], 0)
})
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

let isLoading = ref(true)

const boxScoreSummarycacheService = new CacheService<BoxScoreSummary>({
    ttlSeconds: 900,
    maxItems: 10,
    cacheFilter: (_, data: unknown): data is BoxScoreSummary => isBoxScoreSummary(data),
})

const boxScoreSummary = ref<BoxScoreSummary>({
    game_date_jst: new Date(),
    home: {
        team_id: 0,
        abbreviation: '',
        logo: '',
        players: []
    },
    away: {
        team_id: 0,
        abbreviation: '',
        logo: '',
        players: []
    }
})

const boxScoreData = ref<BoxScoreData>({})
boxScoreSummarycacheService.getOrFetch(Number(props.gameId), () => getBoxScoreSummary(props.gameId))
    .then((response) => {
        boxScoreSummary.value = response
        gameSummary.value.status_text = response.game_date_jst.toISOString().slice(0, 10)
        const players = [...response.home.players, ...response.away.players]
        players.forEach(player => {
            if (!player.is_inactive) boxScoreData.value[player.player_id] = new Array(BOX_SCORE_COLUMNS.length - 1).fill(0)
        })
        isLoading.value = false
    })

const boxScoreRawDatacacheService = new CacheService<BoxScoreRawData>({
    ttlSeconds: 900,
    maxItems: 5,
    cacheFilter: (_, data: unknown): data is BoxScoreRawData => isBoxScoreRawData(data),
})
const boxScoreRawData = ref<BoxScoreRawData>({})
boxScoreRawDatacacheService.getOrFetch(Number(props.gameId), () => getBoxScoreRawData(props.gameId))
    .then((response) => {
        boxScoreRawData.value = response
    })

const updateBoxScoreData = (start_range: number, end_range: number) => {
    if (start_range > end_range) {
        throw new Error("invalid game clock range, start > end")
    }
    for (const [player_id_str, box_score_raw] of Object.entries(boxScoreRawData.value)) {
        const player_id = parseInt(player_id_str, 10)
        let start_box_score: number[] | null = null
        let end_box_score: number[] | null = null
        for (let i = 0; i < box_score_raw.length; i++) {
            const [time, box_score] = box_score_raw[i]
            if (time >= start_range) {
                if (!start_box_score) {
                    if (i == 0) {
                        start_box_score = new Array(BOX_SCORE_COLUMNS.length - 1).fill(0)
                    } else {
                        start_box_score = box_score_raw[i - 1][1]
                    }
                }
                if (time <= end_range) {
                    if (i == 0) {
                        end_box_score = new Array(BOX_SCORE_COLUMNS.length - 1).fill(0)
                    } else {
                        end_box_score = box_score
                    }
                } else {
                    break
                }
            }
        }
        if (!start_box_score || !end_box_score) {
            boxScoreData.value[player_id] = convertPlayTimeToMin(calcShootingPercentage(new Array(BOX_SCORE_COLUMNS.length - 1).fill(0)))
        } else {
            boxScoreData.value[player_id] = convertPlayTimeToMin(calcShootingPercentage(end_box_score.map((v, i) => v - start_box_score[i])))
        }
    }
}

const calcShootingPercentage = (boxScoraRow: number[]) => {
    let result = boxScoraRow
    if (result.length < 15) {
        throw new Error("invalid box score data row")
    }

    if (boxScoraRow[7] !== 0) {
        result[8] = Math.round((boxScoraRow[6] / boxScoraRow[7]) * 100 * 10) / 10
    } else {
        result[8] = 0
    }

    if (boxScoraRow[10] !== 0) {
        result[11] = Math.round((boxScoraRow[9] / boxScoraRow[10]) * 100 * 10) / 10
    } else {
        result[11] = 0
    }

    if (boxScoraRow[13] !== 0) {
        result[14] = Math.round((boxScoraRow[12] / boxScoraRow[13]) * 100 * 10) / 10
    } else {
        result[14] = 0
    }
    return result
}

const convertPlayTimeToMin = (boxScoraRow: number[]) => {
    let result = boxScoraRow
    result[0] = Math.round(boxScoraRow[0] / 60 * 10) / 10
    return result
}

</script>


<style scoped>
.container {
    background-color: var(--main-backgroud-color);
    color: #fff;
    height: calc(100% - var(--footer-height));
    display: flex;
    flex-direction: column;
}

.tab-menu {
    display: flex;
}

.tab {
    flex: 1;
    display: grid;
    text-align: center;
    align-items: center;
    color: rgba(255, 255, 255, 0.5);
    font-size: large;
    padding-bottom: 4px;
}

.tab.selected {
    color: rgba(255, 255, 255, 1);
    border-bottom: 4px solid rgba(200, 50, 50, 0.9);
}

.game-clock {
    display: flex;
    flex-direction: column;
    margin: 20px 50px 0px 50px;
    align-items: center;
}

.game-clock-slider {
    width: 100% !important;
    user-select: auto !important;
}
</style>
