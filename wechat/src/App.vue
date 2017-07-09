<template>
  <div id="app">
    <transition name="router-fade" mode="out-in">
      <router-view></router-view>
    </transition>
    <alert v-model="lackPhone" @on-hide="alertHide">请您先绑定手机享受全部服务</alert>
  </div>
</template>

<script>
import { mapActions, mapState } from 'vuex'
import { Alert } from 'vux'
import './style/common.css'

export default {
  name: 'app',
  components: {
    Alert
  },
  data () {
    return {
      wxSign: {}
    }
  },
  mounted () {
    this.testLocal()
    this.getAccountsInfo()
    this.getSign()
  },
  computed: {
    ...mapState({
      havePhone: 'havePhone'
    }),
    errorMsg () {
      return this.$store.state.errorMsg
    },
    lackPhone () {
      let havePhone = Boolean(this.havePhone)
      return !havePhone
    }
  },
  watch: {
    errorMsg (newOne, oldOne) {
      this.$vux.toast.show({
        text: newOne
      })
    }
  },
  methods: {
    ...mapActions({
      getAccountsInfo: 'getAccountsInfo'
    }),
    testLocal () {
      if (process.env.NODE_ENV === 'development') {
        this.$http.get('test_page/').then(res => {
          console.log('test_page')
        })
      }
    },
    getSign () {
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
    },
    alertHide () {
      // console.log('hide')
      this.$router.push('/person/phone')
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
