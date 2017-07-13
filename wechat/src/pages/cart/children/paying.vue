<template lang="html">
  <div class="children-container">
    <img :src="currentQRInfo.url" alt="QRCode" class="qrcode">
    <div class="confirm-container">
      <p class="confirm-status">{{ isConfirmed ? ' 确认成功' :'等待管理员确认'}}</p>
      <div class="btn-container">
        <button :disabled="!isConfirmed" class="i-btn i-btn-lg">支付</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import { Popup, XButton } from 'vux'
export default {
  components: {
    Popup,
    XButton
  },
  props: {
    QRInfo: Object
  },
  computed: {
    ...mapState({
      'currentQRInfo': 'QRInfo'
    })
  },
  data () {
    return {
      isPaying: false,
      isConfirmed: false
    }
  },
  mounted () {
    this.getConfirm()
  },
  methods: {
    getConfirm () {
      this.$http.get(`/library/confirm_info/${this.currentQRInfo.pay_id}`).then(res => {
        if (res.data.confirm) {
          this.isConfirmed = true
        } else {
          setTimeout(() => {
            this.getConfirm()
          }, 500)
        }
      }).catch(err => {
        setTimeout(() => {
          this.getConfirm()
        }, 500)
        console.log(err.response.data)
      })
    },
    pay () {
      this.$http.get(`/library/pay/6${this.currentQRInfo.pay_id}`).then(res => {
        if (res.data.error_code === 94) {
          this.$vux.toast.show({
            text: '支付失败'
          })
        } else if (res.data.error_code === 0) {
          this.$vux.toast.show({
            text: '支付成功'
          })
        } else if (res.data.error_code === 111) {
          this.$vux.toast.show({
            text: '金额不足'
          })
        }
      }).catch(err => console.log(err.response.data))
    }
  }
}
</script>

<style lang="css" scoped>
.qrcode {
  width: 100%;
}
.btn-container {
  display: flex;
  justify-content: center;
}
.confirm-status {
  padding: 5px 15px;
}
</style>
