import { defineStore } from "pinia";

import { type RgbaColor } from "../core/colorControl";
import { type quarterRangeVariations } from "../types/QuarterRangeVariations";
import { DEFAULT_THEME_COLOR_BASE } from "../vuetify";

interface SettingsState {
  scoreDisplay: boolean;
  defaultQuarterRangeType: quarterRangeVariations;
  themeColor: RgbaColor;
}

export const settingsStore = defineStore("settings", {
  state: (): SettingsState => ({
    scoreDisplay: true,
    defaultQuarterRangeType: "all",
    themeColor: DEFAULT_THEME_COLOR_BASE,
  }),
  persist: true,
});
