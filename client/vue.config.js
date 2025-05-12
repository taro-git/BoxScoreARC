const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    host: '0.0.0.0',         // どこからのアクセスでも受け入れる
    allowedHosts: 'all'      // ホストチェックを無効化（安全な方法）
  }
})
