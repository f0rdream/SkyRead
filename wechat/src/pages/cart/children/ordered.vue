<template lang="html">
  <div class="children-container">
    <h3>等待状态</h3>
    <book-cell v-for="(book,index) in orderedCart.pending" :key="book.id">
      <p slot="book-title">{{ book.title }}</p>
      <p slot="book-info">{{ book.borrow_time}}</p>
    </book-cell>
    <h3>预定成功</h3>
    <book-cell v-for="(book,index) in orderedCart.success" :key="book.id">
      <input slot="book-checker" type="checkbox" :value="book.id" v-model="checkedCells">
      <p slot="book-title">{{ book.title }}</p>
      <p slot="book-info">{{ book.order_time }}</p>
      <x-button slot="right" @click.native="genQR(book.qrcode)">生成二维码</x-button>
    </book-cell>
    <!-- <x-button @click.native="genQR(checkedCells)" :disabled="allQRAvailble">生成二维码</x-button> -->
  </div>
</template>

<script>
import BookCell from '@/components/BookCell'
import { XButton } from 'vux'
import { mapActions, mapState } from 'vuex'

export default {
  components: {
    BookCell,
    XButton
  },
  data () {
    return {
      checkedCells: []
    }
  },
  computed: {
    allQRAvailble () {
      if (this.checkedCells.length !== 0) {
        return false
      }
      return true
    },
    ...mapState({
      'orderedCart': 'orderedCart'
    })
  },
  mounted () {
    this.getData()
  },
  methods: {
    ...mapActions({
      getData: 'getOrdered'
    })
  }
}
</script>

<style lang="css" scoped>
</style>
