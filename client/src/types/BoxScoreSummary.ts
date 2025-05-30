export interface Player {
  player_id: number
  name: string
  jersey: string
  position: string
  is_inactive: boolean
  sequence: number
}

export interface TeamSummary {
  team_id: number
  abbreviation: string
  logo: string
  players: Player[]
}

export interface BoxScoreSummary {
  game_date_jst: Date
  home: TeamSummary
  away: TeamSummary
}
