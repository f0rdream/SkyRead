<template lang="html">
  <div class="children-container">
    <group title="预约取书">
      <datetime :title="'取书时间'" v-model="orderTime" :start-date="todayString"></datetime>
    </group>
    <div class="btn-container">
      <button class="i-btn" @click="submit">提交</button>
    </div>
  </div>
</template>

<script>
import { Cell, Group, Datetime } from 'vux'
import { mapActions } from 'vuex'
import { timeJS2PY } from '@/config/utils'

export default {
  components: {
    Cell,
    Group,
    Datetime
  },
  data () {
    return {
      orderTime: ''
    }
  },
  computed: {
    todayString () {
      let today = new Date()
      return `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
    }
  },
  methods: {
    ...mapActions({
      submitAct: 'orderTime'
    }),
    submit () {
      let orderTime = new Date(this.orderTime)
      let form = {
        book_id: this.$route.params.bookId,
        order_time: timeJS2PY(orderTime),
        isbn13: this.$route.params.isbn13
      }
      this.submitAct(form)
    }
  }
}
</script>

<style lang="css">
</style>
