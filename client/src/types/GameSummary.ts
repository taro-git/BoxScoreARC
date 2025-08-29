export interface Player {
    playerId: number
    name: string
    jersey: string
    position: string
    isStarter: boolean
    isInactive: boolean
    sequence: number
}

interface Team {
    teamId: number
    abbreviation: string
    logo: string
}

export interface IGameSummary {
    gameId: string
    homePlayers: Player[]
    awayPlayers: Player[]
    homeTeam: Team
    awayTeam: Team
    sequence: number
    statusId: number
    statusText: string
    gameDatetime: string
    homeScore: number
    awayScore: number
    gameCategory: string
}

export class GameSummary {
    gameId: string
    homePlayers: Player[]
    awayPlayers: Player[]
    homeTeam: Team
    awayTeam: Team
    sequence: number
    /**
     * 1: scheduled, 2: game started, 3: game finished
     */
    statusId: number
    statusText: string
    gameDatetime: Date
    homeScore: number
    awayScore: number
    gameCategory: string

    constructor(data?: IGameSummary) {
        this.gameId = data?.gameId ?? ''
        this.homePlayers = data?.homePlayers ?? []
        this.awayPlayers = data?.awayPlayers ?? []
        this.homeTeam = data?.homeTeam ?? { teamId: -1, abbreviation: 'unknown', logo: '' }
        this.awayTeam = data?.awayTeam ?? { teamId: -2, abbreviation: 'unknown', logo: '' }
        this.sequence = data?.sequence ?? 100
        this.statusId = data?.statusId ?? 3
        this.statusText = data?.statusText ?? ''
        this.gameDatetime = data?.gameDatetime ? new Date(data?.gameDatetime) : new Date()
        this.homeScore = data?.homeScore ?? 0
        this.awayScore = data?.awayScore ?? 0
        this.gameCategory = data?.gameCategory ?? ''
    }
}
