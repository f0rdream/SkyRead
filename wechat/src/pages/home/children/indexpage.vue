<template lang="html">
  <main class="main-part">
    <swiper :list="imgList"></swiper>
  </main>
</template>

<script>
import { Swiper } from 'vux'
export default {
  components: {
    Swiper
  },
  data () {
    return {
      imgList: ['../../assets/logo.png', '../../assets/logo.png', '../../assets/logo.png']
    }
  }
}
</script>

<style lang="css">
</style>
