import axios from 'axios'

import { BoxScoreSummary } from '@/types/BoxScoreSummary'
import { BoxScoreRawData } from '@/types/BoxScore'

const API_BASE_URL = 'http://172.16.0.62:1026/api/nba'

export const getBoxScoreSummary = async (gameId: string): Promise<BoxScoreSummary> => {
    const response = await axios.get(`${API_BASE_URL}/box-score-summary/`, {
        params: {
            gameId: gameId
        }
    })
    return {
        game_date_jst: new Date(response.data.game_date_jst),
        home: response.data.home,
        away: response.data.away
    }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isBoxScoreSummary = (item: any) => {
    return typeof item === 'object' &&
        item !== null &&
        item.game_date_jst instanceof Date &&
        typeof item.home === 'object' &&
        typeof item.home.team_id === 'number' &&
        typeof item.home.abbreviation === 'string' &&
        typeof item.home.logo === 'string' &&
        typeof item.home.players === 'object' &&
        typeof item.away === 'object' &&
        typeof item.away.team_id === 'number' &&
        typeof item.away.abbreviation === 'string' &&
        typeof item.away.logo === 'string' &&
        typeof item.away.players === 'object'
}

export const getBoxScoreRawData = async (gameId: string): Promise<BoxScoreRawData> => {
    const response = await axios.get(`${API_BASE_URL}/box-score-data/`, {
        params: {
            gameId: gameId
        }
    })
    const boxScoreRawData: BoxScoreRawData = {}
    for (const key in response.data) {
        const numericKey = Number(key)
        boxScoreRawData[numericKey] = response.data[key]
    }
    return boxScoreRawData
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isBoxScoreRawData = (item: any) => {
    if (typeof item !== 'object' || item === null || Array.isArray(item)) {
        return false;
    }

    for (const key in item) {
        if (isNaN(Number(key))) return false;

        const value = item[key];
        if (!Array.isArray(value)) return false;

        for (const tuple of value) {
            if (
                !Array.isArray(tuple) ||
                tuple.length !== 2 ||
                typeof tuple[0] !== 'number' ||
                !Array.isArray(tuple[1]) ||
                !tuple[1].every((n) => typeof n === 'number')
            ) {
                return false;
            }
        }
    }

    return true;
};


