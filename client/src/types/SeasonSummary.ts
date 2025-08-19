const Conference = {
    West: 'West',
    East: 'East',
} as const
type Conference = (typeof Conference)[keyof typeof Conference]
export const conferences = Object.values(Conference)

const Division = {
    Northwest: 'Northwest',
    Pacific: 'Pacific',
    Southwest: 'Southwest',
    Atlantic: 'Atlantic',
    Central: 'Central',
    Southeast: 'Southeast',
}
type Division = (typeof Division)[keyof typeof Division]
export const divisions = Object.values(Division)

interface IRegularSeasonTeamStats {
    id: number,
    reb: number,
    eff: number,
    teamAbbreviation: string,
    teamLogo: string,
    conference: Conference,
    conferenceRank: number,
    division: Division,
    divisionRank: number,
    win: number,
    lose: number,
    pts: number,
    ast: number,
    stl: number,
    blk: number,
    fg: number,
    fga: number,
    three: number,
    threea: number,
    ft: number,
    fta: number,
    oreb: number,
    dreb: number,
    to: number,
    pf: number,
    plusminus: number,
    teamId: number,
    season: string,
}

export interface ISeasonSummary {
    season: string,
    regularSeasonTeamsStats: IRegularSeasonTeamStats[]
}

export interface RegularSeasonTeamStats {
    teamAbbreviation: string,
    teamLogo: string,
    conference: Conference,
    conferenceRank: number,
    division: Division,
    divisionRank: number,
    win: number,
    lose: number,
    pct: number,
    gb: number,
}

export class SeasonSummary {
    season: string
    regularSeasonTeamsStats: RegularSeasonTeamStats[]

    constructor(data?: ISeasonSummary) {
        this.season = data?.season ?? ''
        this.regularSeasonTeamsStats = []
        if (data) {
            const westMaxDiff = data.regularSeasonTeamsStats.reduce((max, item) => {
                const diff = item.win - item.lose
                return diff > max && item.conference == Conference.West ? diff : max
            }, -Infinity)
            const eastMaxDiff = data.regularSeasonTeamsStats.reduce((max, item) => {
                const diff = item.win - item.lose
                return diff > max && item.conference == Conference.East ? diff : max
            }, -Infinity)
            for (const regularSeasonTeamStats of data?.regularSeasonTeamsStats) {
                const win = regularSeasonTeamStats.win
                const lose = regularSeasonTeamStats.lose
                const maxDiff = regularSeasonTeamStats.conference == Conference.West ? westMaxDiff : eastMaxDiff
                this.regularSeasonTeamsStats.push({
                    teamAbbreviation: regularSeasonTeamStats.teamAbbreviation,
                    teamLogo: regularSeasonTeamStats.teamLogo,
                    conference: regularSeasonTeamStats.conference,
                    conferenceRank: regularSeasonTeamStats.conferenceRank,
                    division: regularSeasonTeamStats.division,
                    divisionRank: regularSeasonTeamStats.divisionRank,
                    win: win,
                    lose: lose,
                    pct: win + lose > 0 ? Math.round(win / (win + lose) * 10) / 10 : 0,
                    gb: (maxDiff - (win - lose)) / 2
                })
            }
        }
    }
}
