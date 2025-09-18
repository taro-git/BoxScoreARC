import { GameSummary, type IGameSummary } from "../types/GameSummary";
import { BackendApi } from "./backend.api";

function formatDateToYYYYMMDD(dateArg: Date): string {
  const year = dateArg.getFullYear();
  const month = String(dateArg.getMonth() + 1).padStart(2, "0");
  const date = String(dateArg.getDate()).padStart(2, "0");
  return `${year}-${month}-${date}`;
}

export class GameSummariesApi extends BackendApi {
  constructor() {
    super();
    this.setPath("game_summaries");
  }

  public async getGameSummariesByDate(date: Date): Promise<GameSummary[]> {
    const response: IGameSummary[] = await this.get({
      game_datetime: formatDateToYYYYMMDD(date),
    });
    return response.map((iGameSummary) => new GameSummary(iGameSummary));
  }

  public async getGameSummaryByGameId(gameId: string): Promise<GameSummary[]> {
    const response: IGameSummary[] = await this.get({ game_id: gameId });
    return response.map((iGameSummary) => new GameSummary(iGameSummary));
  }

  public async getGameSummaryByMatchUp(
    teamIds: [number, number],
  ): Promise<GameSummary[]> {
    const response1: IGameSummary[] = await this.get({
      home_team_id: teamIds[0],
      away_team_id: teamIds[1],
    });
    const response2: IGameSummary[] = await this.get({
      home_team_id: teamIds[1],
      away_team_id: teamIds[0],
    });
    return [...response1, ...response2].map(
      (iGameSummary) => new GameSummary(iGameSummary),
    );
  }
}
