export const BoxScoreColumnKeys = [
  "pos",
  "min",
  "pts",
  "reb",
  "ast",
  "stl",
  "blk",
  "fg",
  "fga",
  "fgper",
  "three",
  "threea",
  "threeper",
  "ft",
  "fta",
  "ftper",
  "oreb",
  "dreb",
  "to",
  "pf",
  "eff",
  "plusminus",
] as const;
export type BoxScoreColumnKeys = (typeof BoxScoreColumnKeys)[number];
export const BOX_SCORE_COLUMNS: Record<BoxScoreColumnKeys, string> = {
  pos: "POS",
  min: "MIN",
  pts: "PTS",
  reb: "REB",
  ast: "AST",
  stl: "STL",
  blk: "BLK",
  fg: "FG",
  fga: "FGA",
  fgper: "FG%",
  three: "3P",
  threea: "3PA",
  threeper: "3P%",
  ft: "FT",
  fta: "FTA",
  ftper: "FT%",
  oreb: "OREB",
  dreb: "DREB",
  to: "TO",
  pf: "PF",
  eff: "EFF",
  plusminus: "+/-",
};

export interface BoxScoreTableData {
  [key: number]: number[];
}

type boxScoreData = [
  /** elapsedSeconds */
  number,
  /** isOnCourt */
  boolean,
  /** min */
  number,
  /** pts */
  number,
  /** reb */
  number,
  /** ast */
  number,
  /** stl */
  number,
  /** blk */
  number,
  /** fg */
  number,
  /** fga */
  number,
  /** three */
  number,
  /** threea */
  number,
  /** ft */
  number,
  /** fta */
  number,
  /** oreb */
  number,
  /** dreb */
  number,
  /** to */
  number,
  /** pf */
  number,
  /** eff */
  number,
  /** plusminus */
  number,
];

export interface PlayerOnBoxScore {
  playerId: number;
  boxScoreData: boxScoreData[];
}

export interface IBoxScore {
  gameId: string;
  finalPeriod: number;
  isCollect: boolean;
  boxScoreDataHeader: string[];
  homePlayers: PlayerOnBoxScore[];
  awayPlayers: PlayerOnBoxScore[];
}

export class BoxScore {
  gameId: string;
  finalPeriod: number;
  isCollect: boolean;
  homePlayers: PlayerOnBoxScore[];
  awayPlayers: PlayerOnBoxScore[];

  constructor(data?: IBoxScore) {
    this.gameId = data?.gameId ?? "";
    this.finalPeriod = data?.finalPeriod ?? 4;
    this.isCollect = data?.isCollect ?? false;
    this.homePlayers = data?.homePlayers ?? [];
    this.awayPlayers = data?.awayPlayers ?? [];
  }
}

export interface BoxScoreRow {
  playerId: number;
  playerName: string;
  jersey: string;
  pos: string;
  isInactive: boolean;
  comulativeBoxscore: number[];
}
