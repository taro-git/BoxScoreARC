import { isBoxScoreSummary, type BoxScoreSummary } from "../types/BoxScoreSummary";
import { BackendApi } from "./backend";

export class BoxScoreSummaryApi extends BackendApi {
    constructor() {
        super()
        this.setPath('/nba/box-score-summary')
    }

    public async getBoxScoreSummary(gameId: string): Promise<BoxScoreSummary> {
        return await this.get({ gameId: gameId }, isBoxScoreSummary)
    }
}

