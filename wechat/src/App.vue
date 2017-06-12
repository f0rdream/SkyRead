<template>
  <div id="app">
    <transition name="router-fade" mode="out-in">
      <router-view></router-view>
    </transition>
  </div>
</template>

<script>
import './style/common.css'
export default {
  name: 'app',
  data () {
    return {
      wxSign: {}
    }
  },
  mounted () {
    this.testLocal()
    this.getSign()
  },
  methods: {
    testLocal () {
      this.$http.get('test_page/').then(res => {
        console.log('test_page')
      })
    },
    getSign () {
      // let url = encodeURIComponent('http://skyread.fordream001.cn')
      let url = encodeURIComponent(location.href.split('#')[0])
      this.$http.get(`signature?url=${url}`).then(res => {
        this.wxSign = res.data
        this.$wechat.config({
          debug: true,
          appId: this.wxSign.appId || 'wx06e40e988b339f37',
          timestamp: this.wxSign.timestamp,
          nonceStr: this.wxSign.nonceStr,
          signature: this.wxSign.signature,
          jsApiList: ['scanQRCode']
        })
        this.$wechat.ready(function () {
          console.log('wechatOk')
        })
      }).catch(err => {
        console.warn(err)
      })
    }
  }
}
</script>

<style lang="less">
@import '~vux/src/styles/reset.less';
@import '~vux/src/styles/1px.less';

#app {
  height: 100%;
}
</style>
