import { createVuetify } from "vuetify";
import * as components from "vuetify/components";
import * as directives from "vuetify/directives";
import { aliases, mdi } from "vuetify/iconsets/mdi";
import "vuetify/styles";

import {
  baseToAccent,
  baseToDarken,
  baseToLighten,
  type RgbaColor,
} from "./core/colorControl";

export const DEFAULT_THEME_COLOR_BASE: RgbaColor = "#42B883ff";

export const vuetify = createVuetify({
  components,
  directives,
  icons: {
    defaultSet: "mdi",
    aliases,
    sets: { mdi },
  },
  theme: {
    defaultTheme: "myCustomTheme",
    themes: {
      myCustomTheme: {
        dark: false,
        colors: {
          base: DEFAULT_THEME_COLOR_BASE,
          darken: baseToDarken(DEFAULT_THEME_COLOR_BASE),
          lighten: baseToLighten(DEFAULT_THEME_COLOR_BASE),
          accent: baseToAccent(DEFAULT_THEME_COLOR_BASE),
        },
      },
    },
  },
  locale: {
    locale: "ja",
    fallback: "en",
    messages: { ja: { $vuetify: { close: "閉じる" } } },
  },
});
