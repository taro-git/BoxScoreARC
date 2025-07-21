// export interface GameSummary {
//     game_id: string
//     home_team: string
//     home_logo: string
//     home_score?: number
//     away_team: string
//     away_logo: string
//     away_score?: number
//     status_text: string
//     status_id: number
//     live_period: number
//     live_clock: string
//     game_category: string
// }


export class GameSummary {
    game_id: string
    home_team: string
    home_logo: string
    home_score?: number
    away_team: string
    away_logo: string
    away_score?: number
    status_text: string
    status_id: number
    live_period: number
    live_clock: string
    game_category: string

    constructor(data?: GameSummary) {
        this.game_id = data?.game_id ?? ''
        this.home_team = data?.home_team ?? ''
        this.home_logo = data?.home_logo ?? ''
        this.home_score = data?.home_score
        this.away_team = data?.away_team ?? ''
        this.away_logo = data?.away_logo ?? ''
        this.away_score = data?.away_score
        this.status_text = data?.status_text ?? ''
        this.status_id = data?.status_id ?? 0
        this.live_period = data?.live_period ?? 0
        this.live_clock = data?.live_clock ?? ''
        this.game_category = data?.game_category ?? ''
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
