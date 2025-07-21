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

export class BoxScoreSummary {
    game_date_jst: Date
    home: TeamSummary
    away: TeamSummary

    constructor(data?: BoxScoreSummary) {
        this.game_date_jst = data?.game_date_jst ?? new Date()
        this.home = data?.home ?? {
            team_id: 0,
            abbreviation: '',
            logo: '',
            players: []
        }
        this.away = data?.away ?? {
            team_id: 0,
            abbreviation: '',
            logo: '',
            players: []
        }
    }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export const isBoxScoreSummary = (item: any) => {
    return typeof item === 'object' &&
        item !== null &&
        typeof item.game_date_jst === 'string' &&
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
