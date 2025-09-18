export type RgbaColor = string;

export function isValidRgbaColor(str: string): str is RgbaColor {
  return /^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$/.test(str);
}

function hexToRgba(hex: RgbaColor): {
  r: number;
  g: number;
  b: number;
  a: number;
} {
  let raw = hex.slice(1);
  if (raw.length == 6) raw = raw + "ff";
  if (raw.length !== 8) throw new Error("Invalid RgbaHex: " + hex);

  const r = parseInt(raw.slice(0, 2), 16);
  const g = parseInt(raw.slice(2, 4), 16);
  const b = parseInt(raw.slice(4, 6), 16);
  const a = parseInt(raw.slice(6, 8), 16);
  return { r, g, b, a };
}

function rgbaToHex({
  r,
  g,
  b,
  a,
}: {
  r: number;
  g: number;
  b: number;
  a: number;
}): RgbaColor {
  const toHex = (n: number) => n.toString(16).padStart(2, "0");
  return `#${toHex(r)}${toHex(g)}${toHex(b)}${toHex(a)}` as RgbaColor;
}

function convertColor(color: RgbaColor, ratio: number): RgbaColor {
  const rgba = hexToRgba(color);

  const convertedR = Math.max(0, Math.min(255, Math.floor(rgba.r * ratio)));
  const convertedG = Math.max(0, Math.min(255, Math.floor(rgba.g * ratio)));
  const convertedB = Math.max(0, Math.min(255, Math.floor(rgba.b * ratio)));
  const convertedA = Number(rgba.a);

  return rgbaToHex({
    r: convertedR,
    g: convertedG,
    b: convertedB,
    a: convertedA,
  });
}

export function baseToDarken(color: RgbaColor): RgbaColor {
  return convertColor(color, 0.85);
}

export function baseToLighten(color: RgbaColor): RgbaColor {
  return convertColor(color, 1.15);
}

function invertColor(color: RgbaColor): RgbaColor {
  const { r, g, b, a } = hexToRgba(color);

  const invertedR = 255 - r;
  const invertedG = 255 - g;
  const invertedB = 255 - b;

  return rgbaToHex({ r: invertedR, g: invertedG, b: invertedB, a });
}

export function baseToAccent(color: RgbaColor): RgbaColor {
  return invertColor(color);
}
