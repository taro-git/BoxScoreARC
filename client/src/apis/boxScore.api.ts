import { BoxScore, type IBoxScore } from "../types/BoxScore";
import { BackendApi } from "./backend.api";

export class BoxScoreApi extends BackendApi {
    constructor() {
        super()
        this.setPath('box_score')
    }

    public async getBoxScore(gameId: string): Promise<BoxScore[]> {
        const result: IBoxScore[] = await this.get({ game_id: gameId })
        return result.map((iBoxScore: IBoxScore) => new BoxScore(iBoxScore))
    }
}

