<template lang="html">
  <div class="children-container">
    <group class="child-container">
      <x-input title="新手机号码" v-model="phoneNum"></x-input>
      <x-input title="发送验证码" v-model="captcha">
          <x-button slot="right" type="primary" mini @click.native="sendMsg">发送验证码</x-button>
      </x-input>
    </group>
    <x-button type="primary btn-gap" @click.native="bindPhone">绑定手机号码</x-button>
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
      hasSend: false
    }
  },
  methods: {
    sendMsg () {
      this.$http.post('accounts/send/', { phone_number: this.phoneNum }, {
        // headers: {'X-CSRFToken': '4YoLA5dqALSjNZ4bVwE57hlXu9iVVuoK'}
        xsrfCookieName: 'csrftoken',
        xsrfHeaderName: 'X-CSRFToken'
      }).then(res => {
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
    }
  }
}
</script>

<style lang="css">
.btn-gap {
  margin-top: .15rem;
}
</style>
