const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  publicPath: '/view/',
  devServer: {
    host: '0.0.0.0',         // どこからのアクセスでも受け入れる
    allowedHosts: 'all',     // ホストチェックを無効化（安全な方法）
    historyApiFallback: {
        rewrites: [
            {from: /^\/view/, to: '/view/index.html'},
        ]
    }
  },
  configureWebpack: {
    watchOptions :{
      aggregateTimeout: 300,
      poll: 1000
    }
  },
  chainWebpack: config => {
    config.plugin('html').tap(args => {
        args[0].title = 'Box Score ARC'
        return args
    })
  }
})
