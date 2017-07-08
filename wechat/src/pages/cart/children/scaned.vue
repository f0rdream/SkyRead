<template lang="html">
  <div class="children-container">
    <book-cell v-for="(book,index) in bookList" :key="book.id">
      <!-- <div class="weui-cell__hd" slot="book-checker"><input type="checkbox"  class="weui-check"> <i class="weui-icon-checked vux-checklist-icon-checked"></i></div> -->
      <!-- <input slot="book-checker" type="checkbox" :value="book.id" v-model="checkedCells" class="weui-check"> -->
      <!-- <label slot="book-checker" class="i-checker-container" type="checkbox" :value="book.id">
        <input type="checkbox" class="i-checker-input" v-model="checkedCells">
        <i class="i-checker-icon"></i>
      </label> -->
      <check-box slot="book-checker" :value="book.id" v-model="checkedCells"></check-box>
      <p slot="book-title" class="book-title">{{ book.title }}</p>
      <p slot="book-info" class="book-info">借书时间: {{ book.borrow_time }}</p>
      <p slot="book-info" class="book-info">还书时间: {{ book.borrow_time }}</p>
      <button slot="right" class="i-btn multi-btn" @click="genQR([book.id])" >借书码</button>
      <button slot="right" class="i-btn multi-btn" @click="delScaned(book.id, index)">删除</button>
    </book-cell>
    <div class="btn-bottom-container">
      <button @click.native="genQR(checkedCells)" :disabled="allQRAvailble" class="i-btn" v-if="bookList.length > 0">批量生成借书码</button>
    </div>

  </div>
</template>

<script>
import BookCell from '@/components/BookCell'
import { XButton } from 'vux'
import CheckBox from '@/components/CheckBox'
import { mapActions, mapState } from 'vuex'
// import ClickableList from '@/components/ClickableList'

export default {
  components: {
    BookCell,
    XButton,
    CheckBox
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

<style scoped>
.btn-bottom-container {
  display: flex;
  justify-content: center;
  margin: 15px 10px;
}
</style>
