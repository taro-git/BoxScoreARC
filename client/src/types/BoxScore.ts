export const BOX_SCORE_COLUMNS = [
  'POS', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FG', 'FG%', '3P', '3P%', 'FT', 'FT%', 'OREB', 'DREB', 'TO', 'PF', 'EFF', '+/-'
]

interface BoxScoreColumns {
  min: number
  pts: number
  reb: number
  ast: number
  stl: number
  blk: number
  fg: number
  fg_percent: number
  three: number
  three_percent: number
  ft: number
  ft_percent: number
  oreb: number
  dreb: number
  to: number
  pf: number
  eff: number
  plus_minus: number
}

export interface BoxScoreRow {
  player_id: number
  player_name: string
  jersey: string
  pos: string
  // number は試合の経過時間 milli sec, number を昇順ソートしておく想定
  comulative_boxscore: number[]//Array<[number, BoxScoreColumns]>
}

export interface BoxScore {
    home: BoxScoreRow[]
    away: BoxScoreRow[]
}

