<template lang="html">
  <div class="children-container">
    <img :src="currentQRInfo.url" alt="QRCode" class="qrcode">
    <div class="confirm-status">
      {{ isConfirmed ? ' 确认成功' :'等待管理员确认'}}
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
      isConfirmed: false
    }
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
    }
  }
}
</script>

<style lang="css" scoped>
.qrcode {
  width: 100%;
}
.confirm-status {
  padding: 5px 15px;
}
</style>
