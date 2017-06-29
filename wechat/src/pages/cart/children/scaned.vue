<template lang="html">
  <div class="children-container">
    <book-cell v-for="(book,index) in bookList" :key="book.id">
      <input slot="book-checker" type="checkbox" :value="book.id" v-model="checkedCells">
      <p slot="book-title">{{ book.title }}</p>
      <p slot="book-info">{{ book.borrow_time}}</p>
      <x-button slot="right" @click.native="genQR([book.id])" mini>生成二维码</x-button>
      <x-button slot="right" @click.native="delScaned(book.id, index)" mini>删除</x-button>
    </book-cell>
    <x-button @click.native="genQR(checkedCells)" :disabled="allQRAvailble">生成全部二维码</x-button>
  </div>
</template>

<script>
import BookCell from '@/components/BookCell'
import { XButton } from 'vux'
import { mapActions, mapState } from 'vuex'
// import ClickableList from '@/components/ClickableList'

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
      'bookList': 'scanedCart'
    })
  },
  mounted () {
    this.getData()
  },
  methods: {
    ...mapActions({
      genQR: 'getBorrowQR',
      getData: 'getScanedList',
      delScaned: 'delScanedList'
    })
  }
}
</script>

<style lang="css" scoped>
</style>
