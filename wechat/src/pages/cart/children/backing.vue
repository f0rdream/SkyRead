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
        }
      }).catch(err => {
        this.getConfirm()
        console.log(err)
      })
    }
  }
}
</script>

<style lang="css" scoped>
.qrcode {
  width: 100%;
}
</style>
