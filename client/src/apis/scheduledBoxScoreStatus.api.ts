import { type ScheduledBoxScoreStatus } from "../types/ScheduledBoxScoreStatus";
import { BackendApi } from "./backend.api";

export class ScheduledBoxScoreStatusApi extends BackendApi {
  constructor() {
    super();
    this.setPath("scheduled_box_score_status");
  }

  public async getScheduledBoxScoreStatus(
    gameId: string,
  ): Promise<ScheduledBoxScoreStatus[]> {
    return await this.get({ game_id: gameId });
  }

  public async postScheduledBoxScoreStatus(gameId: string): Promise<void> {
    await this.post({ game_id: gameId });
  }
}
