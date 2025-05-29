export interface GameSummary {
  game_id: string
  home_team?: string
  home_logo: string
  home_score: number
  away_team?: string
  away_logo: string
  away_score: number
  status_text: string
  status_id?: number
  live_period?: number
  live_clock?: string
  game_category?: string
}
