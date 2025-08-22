import { type ISeasonSummary, SeasonSummary } from "../types/SeasonSummary";
import { BackendApi } from "./backend.api";

export class SeasonSummariesApi extends BackendApi {
    constructor() {
        super()
        this.setPath('season_summaries')
    }

    public async getSeasonSummaries(): Promise<SeasonSummary[]> {
        const response: ISeasonSummary[] = await this.get()
        return response.map(iSeasonSummary => new SeasonSummary(iSeasonSummary))
    }
}

