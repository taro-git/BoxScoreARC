import { GameSummary } from '@/types/GameSummary'
import axios from 'axios'

const API_BASE_URL = process.env.VUE_APP_API_BASE_URL

function formatDateToYYYYMMDD(dateArg: Date): string {
    const year = dateArg.getFullYear()
    const month = String(dateArg.getMonth() + 1).padStart(2, '0')
    const date = String(dateArg.getDate()).padStart(2, '0')
    return `${year}${month}${date}`
}

export const getGameSummaries = async (date: Date): Promise<GameSummary[]> => {
    const response = await axios.get(`${API_BASE_URL}/nba/game-summaries/`, {
        params: {
            date: formatDateToYYYYMMDD(date)
        }
    })
    return response.data
}

export const getGameSummary = async (gameId: string): Promise<GameSummary> => {
    // まだ存在しない
    // const response = await axios.get(`${API_BASE_URL}/nba/game-summary/`, {
    //   params: {
    //     gameId: gameId
    // }})
    // return response.data
    return {
        game_id: gameId,
        home_team: "BOS",
        home_logo: "https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg",
        home_score: 100,
        away_team: "CLE",
        away_logo: "https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg",
        away_score: 101,
        status_text: "Final",
        status_id: 3,
        live_period: 4,
        live_clock: "    ",
        game_category: "Playoffs",
    }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isGameSummary = (item: any) => {
    return typeof item === 'object' &&
        item !== null &&
        typeof item.game_id === 'string' &&
        typeof item.home_team === 'string' &&
        typeof item.home_logo === 'string' &&
        (typeof item.home_score === 'number' || item.home_score === null) &&
        typeof item.away_team === 'string' &&
        typeof item.away_logo === 'string' &&
        (typeof item.away_score === 'number' || item.away_score === null) &&
        typeof item.status_id === 'number' &&
        typeof item.status_text === 'string' &&
        typeof item.live_period === 'number' &&
        typeof item.live_clock === 'string' &&
        typeof item.game_category === 'string'
}
