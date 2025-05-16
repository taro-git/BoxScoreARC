import { MatchSummary } from '@/types/MatchSummary'
import axios from 'axios'

const API_BASE_URL = 'http://172.16.0.62:1026/api/nba'

function formatDateToYYYYMMDD(dateArg: Date): string {
  const year = dateArg.getFullYear()
  const month = String(dateArg.getMonth() + 1).padStart(2, '0')
  const date = String(dateArg.getDate()).padStart(2, '0')
  return `${year}${month}${date}`
}

export const getMatchSummaries = async (date: Date): Promise<MatchSummary[]> => {
  const response = await axios.get(`${API_BASE_URL}/game-summaries/`, {
    params: {
      date: formatDateToYYYYMMDD(date)
  }})
  return response.data
}
