import { isBoxScoreRawData, type BoxScoreRawData } from "../types/BoxScore";
import { BackendApi } from "./backend";

export class BoxScoreRawDataApi extends BackendApi {
    constructor() {
        super()
        this.setPath('/nba/box-score-data')
    }

    public async getBoxScoreRawData(gameId: string): Promise<BoxScoreRawData> {
        return await this.get({ gameId: gameId }, isBoxScoreRawData)
    }
}

