import { type GameSummary, isGameSummary } from "../types/GameSummary";
import { BackendApi } from "./backend";

function formatDateToYYYYMMDD(dateArg: Date): string {
    const year = dateArg.getFullYear()
    const month = String(dateArg.getMonth() + 1).padStart(2, '0')
    const date = String(dateArg.getDate()).padStart(2, '0')
    return `${year}${month}${date}`
}

export class GameSummariesApi extends BackendApi {
    constructor() {
        super()
        this.setPath('/nba/game-summaries')
    }

    public async getGameSummaries(date: Date): Promise<GameSummary[]> {
        return await this.get({ date: formatDateToYYYYMMDD(date) }, (data: unknown): data is GameSummary[] => {
            if (!Array.isArray(data)) return false
            else if (data.length === 0) return true
            else return data.every(item => isGameSummary(item) && (item as GameSummary).status_id !== 2)
        })
    }
}

