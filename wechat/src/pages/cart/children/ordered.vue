<template lang="html">
  <div class="children-container">
    <div class="title-container">
      <p class="title">外借中</p>
    </div>
    <book-cell v-for="(book,index) in orderedCart.pending" :key="book.id">
      <p slot="book-title" class="book-title">{{ book.title }}</p>
      <p slot="book-info" class="book-info">还书时间: {{ dateFormat(convert(book.may_return_time), 'YYYY-MM-DD') }}</p>
      <button class="i-btn multi-btn" slot="right" @click="$router.push(`/bookshelf/ordertime/${book.id}/${book.isbn13}`)" :disabled="!book.return_state">预订</button>
      <button class="i-btn multi-btn" slot="right" @click="delOrdered(book.id, WAITTYPE)">删除</button>
    </book-cell>
    <div class="title-container">
      <p class="title">预定成功</p>
    </div>
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
      delOrdered: 'delOrdered',
      genQR: 'getOrderQR'
    }),
    convert: timePY2JS,
    dateFormat
  }
}
</script>

<style lang="css" scoped>
.title {
  display: inline-block;
  font-size: 15px;
  margin: 5px 10px;
  font-weight: 600;
  padding: 2px 5px;
  border-bottom: 2px #2bc1c8 solid;
  color: #5f5f5f;
}
</style>
