/* eslint-disable no-undef */
// prettier.config.js
module.exports = {
  plugins: [require.resolve("@trivago/prettier-plugin-sort-imports")],
  importOrder: [
    "^[a-z]", // 外部ライブラリ (react, vue, lodash など)
    "^@/", // エイリアス (例: @/components, @/utils)
    "^[./]", // 相対パス (./, ../)
  ],
  importOrderSeparation: true, // グループ間で空行を入れる
  importOrderSortSpecifiers: true, // {} 内の並び替えもする
  importOrderCaseInsensitive: true, // 大文字小文字を区別せずソート
};
