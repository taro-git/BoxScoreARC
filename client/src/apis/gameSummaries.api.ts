import { type IGameSummary, GameSummary } from "../types/GameSummary";
import { BackendApi } from "./backend.api";

function formatDateToYYYYMMDD(dateArg: Date): string {
    const year = dateArg.getFullYear()
    const month = String(dateArg.getMonth() + 1).padStart(2, '0')
    const date = String(dateArg.getDate()).padStart(2, '0')
    return `${year}-${month}-${date}`
}

export class GameSummariesApi extends BackendApi {
    constructor() {
        super()
        this.setPath('game_summaries')
    }

    public async getGameSummariesByDate(date: Date): Promise<GameSummary[]> {
        const response: IGameSummary[] = await this.get({ game_datetime: formatDateToYYYYMMDD(date) })
        return response.map(iGameSummary => new GameSummary(iGameSummary))
    }

    public async getGameSummaryByGameId(gameId: string): Promise<GameSummary[]> {
        const response: IGameSummary[] = await this.get({ game_id: gameId })
        return response.map(iGameSummary => new GameSummary(iGameSummary))
    }
}

