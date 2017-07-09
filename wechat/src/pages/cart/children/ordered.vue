<template lang="html">
  <div class="children-container">
    <h3>外借中</h3>
    <book-cell v-for="(book,index) in orderedCart.pending" :key="book.id">
      <p slot="book-title" class="book-title">{{ book.title }}</p>
      <p slot="book-info" class="book-info">还书时间: {{ dateFormat(convert(book.may_return_time), 'YYYY-MM-DD') }}</p>
      <button class="i-btn multi-btn" slot="right" @click="$router.push(`/bookshelf/${book.id}`)" :disabled="!book.return_state">预订</button>
      <button class="i-btn multi-btn" slot="right" @click="delOrdered(book.id, WAITTYPE)">删除</button>
    </book-cell>
    <h3>预定成功</h3>
    <book-cell v-for="(book,index) in orderedCart.success" :key="book.id">
      <check-box slot="book-checker" :value="book.id" v-model="checkedCells"></check-box>
      <!-- <input slot="book-checker" type="checkbox" :value="book.id" v-model="checkedCells"> -->
      <p slot="book-title" class="book-title">{{ book.title }}</p>
      <p slot="book-info" class="book-info">取书时间: {{ dateFormat(convert(book.order_time), 'YYYY-MM-DD') }}</p>
      <button class="i-btn multi-btn" slot="right" @click="genQR(book.qrcode)">取书二维码</button>
      <button class="i-btn multi-btn" slot="right" @click="delOrdered(book.id, SUCCESSTYPE)">取消</button>
    </book-cell>
    <!-- <x-button @click.native="genQR(checkedCells)" :disabled="allQRAvailble">生成二维码</x-button> -->
  </div>
</template>

<script>
import BookCell from '@/components/BookCell'
import CheckBox from '@/components/CheckBox'
import { timePY2JS } from '@/config/utils'
import { XButton, dateFormat } from 'vux'
import { mapActions, mapState } from 'vuex'

export default {
  components: {
    BookCell,
    XButton,
    CheckBox
  },
  data () {
    return {
      checkedCells: [],
      WAITTYPE: 1,
      SUCCESSTYPE: 2
    }
  },
  computed: {
    ...mapState({
      'orderedCart': 'orderedCart'
    })
  },
  mounted () {
    this.getData()
  },
  methods: {
    ...mapActions({
      getData: 'getOrdered',
      delOrdered: 'delOrdered'
    }),
    convert: timePY2JS,
    dateFormat
  }
}
</script>

<style lang="css" scoped>
</style>
