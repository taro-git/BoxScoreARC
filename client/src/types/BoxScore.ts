export const BOX_SCORE_COLUMNS = [
    'POS', 'MIN', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', 'FT', 'FTA', 'FT%', 'OREB', 'DREB', 'TO', 'PF', 'EFF', '+/-'
]

export interface BoxScoreRawData {
    [key: number]: Array<[number, number[]]>
}

export interface BoxScoreData {
    [key: number]: number[]
}

export interface BoxScoreRow {
    player_id: number
    player_name: string
    jersey: string
    pos: string
    is_inactive: boolean
    comulative_boxscore: number[]
}

