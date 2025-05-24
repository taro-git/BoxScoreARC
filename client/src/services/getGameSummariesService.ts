import { GameSummary } from '@/types/GameSummary'
import axios from 'axios'

const API_BASE_URL = 'http://172.16.0.62:1026/api/nba'

function formatDateToYYYYMMDD(dateArg: Date): string {
  const year = dateArg.getFullYear()
  const month = String(dateArg.getMonth() + 1).padStart(2, '0')
  const date = String(dateArg.getDate()).padStart(2, '0')
  return `${year}${month}${date}`
}

export const getgameSummaries = async (date: Date): Promise<GameSummary[]> => {
  const response = await axios.get(`${API_BASE_URL}/game-summaries/`, {
    params: {
      date: formatDateToYYYYMMDD(date)
  }})
  return response.data
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isgameSummary = (item : any) => {
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
  typeof item.live_clock === 'string'
}
