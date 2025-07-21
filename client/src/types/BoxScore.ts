export const BOX_SCORE_COLUMN_KEYS = [
    'pos', 'min', 'pts', 'reb', 'ast', 'stl', 'blk', 'fg', 'fga', 'fgper', 'three', 'threea', 'threeper', 'ft', 'fta', 'ftper', 'oreb', 'dreb', 'to', 'pf', 'eff', 'plusminus'
] as const
export type BoxScoreColumnKeys = typeof BOX_SCORE_COLUMN_KEYS[number]
export const BOX_SCORE_COLUMNS: Record<BoxScoreColumnKeys, string> = {
    pos: 'POS',
    min: 'MIN',
    pts: 'PTS',
    reb: 'REB',
    ast: 'AST',
    stl: 'STL',
    blk: 'BLK',
    fg: 'FG',
    fga: 'FGA',
    fgper: 'FG%',
    three: '3P',
    threea: '3PA',
    threeper: '3P%',
    ft: 'FT',
    fta: 'FTA',
    ftper: 'FT%',
    oreb: 'OREB',
    dreb: 'DREB',
    to: 'TO',
    pf: 'PF',
    eff: 'EFF',
    plusminus: '+/-'
}

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

