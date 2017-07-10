<template lang="html">
  <div class="children-container">
    <img :src="currentQRInfo" alt="QRCode" class="qrcode">
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
