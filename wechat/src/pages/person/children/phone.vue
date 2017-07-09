<template lang="html">
  <div class="children-container">
    <group class="child-container">
      <x-input title="新手机号码" v-model="phoneNum"></x-input>
      <x-input title="发送验证码" v-model="captcha">
        <button slot="right" class="i-btn" @click="sendMsg" :disabled="hasSend">{{hasSend ? `等待${timer}` : '发送验证码'}}</button>
      </x-input>
    </group>
    <div class="btn-container">
      <button class="i-btn i-btn-lg" @click="bindPhone">绑定手机号码</button>
    </div>
  </div>
</template>

<script>
import { XInput, Group, Toast, XButton } from 'vux'
export default {
  components: {
    XInput,
    Group,
    Toast,
    XButton
  },
  data () {
    return {
      phoneNum: '',
      captcha: '',
      hasSend: false,
      timer: 0
    }
  },
  computed: {
  },
  methods: {
    sendMsg () {
      this.$http.post('accounts/send/', { phone_number: this.phoneNum }, {
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken'
      }).then(res => {
        this.hasSend = true
        this.setTimer()
        if (res.data.status === 'success') {
          this.$vux.toast.show({
            text: '已发送'
          })
        } else {
          this.$vux.toast.show({
            text: res.data.error_code
          })
        }
      })
    },
    bindPhone () {
      this.$http.post('accounts/phone/', {phone_num: this.phoneNum, captcha: this.captcha}).then(res => {
        let errorCode = res.data.error_code
        if (errorCode === 1) {
          this.$vux.toast.show({
            text: '验证码错误'
          })
        } else if (errorCode === 2) {
          this.$vux.toast.show({
            text: '发生错误'
          })
        } else if (errorCode === 0) {
          this.$vux.toast.show({
            text: '绑定成功'
          })
        }
      })
    },
    setTimer () {
      if (this.hasSend) {
        this.timer = 60
        let interval = window.setInterval(() => {
          this.timer -= 1
          if (this.timer === 0) {
            window.clearInterval(interval)
            this.hasSend = false
          }
        }, 1000)
      }
    }
  }
}
</script>

<style lang="css" scoped>
.btn-container {
  display: flex;
  justify-content: center;
}
</style>
