import { BoxScoreColumnKeys } from "./BoxScore";

export interface TeamStats {
  boxScoreColumnKey: BoxScoreColumnKeys;
  home: number;
  away: number;
}
