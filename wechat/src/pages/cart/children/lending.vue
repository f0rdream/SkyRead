<template lang="html">
  <div class="children-container">
    <book-cell v-for="(book,index) in bookList" :key="book.id">
      <check-box slot="book-checker" :value="book.id" v-model="checkedCells"></check-box>
      <p slot="book-title" class="book-title">{{ book.title }}</p>
      <p slot="book-info" class="book-info">借书时间: {{ book.borrow_time }}</p>
      <p slot="book-info" class="book-info">归还时间: {{ book.return_time }}</p>
      <p slot="book-info" class="book-info" :class="getStyle(book.due)">剩余时间: {{ book.due }}天</p>
      <button slot="right" @click="reNewRenting(book.id)" class="i-btn multi-btn">续借</button>
      <button slot="right" @click="genQR([book.id])" class="i-btn multi-btn">还书码</button>
    </book-cell>
    <div class="btn-bottom-container">
      <button @click.native="genQR(checkedCells)" :disabled="allQRAvailble" class="i-btn" v-if="bookList.length > 0">批量生成还书码</button>
    </div>
  </div>
</template>

<script>
import BookCell from '@/components/BookCell'
import CheckBox from '@/components/CheckBox'
import { XButton } from 'vux'
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
      'bookList': 'rentingCart'
    })
  },
  mounted () {
    this.getData()
  },
  methods: {
    ...mapActions({
      genQR: 'getRentingQR',
      getData: 'getRentingList',
      reNewRenting: 'reNewRenting'
    }),
    getStyle (day) {
      if (day > 7) {
        return
      } else if (day < 3) {
        return 'due-eager'
      } else {
        return 'dye-normal'
      }
    }
  }
}
</script>

<style lang="css" scoped>
.due-earger {
  color: red;
}
.due-eager {
  color: #2bc6b9;
}
.btn-bottom-container {
  display: flex;
  justify-content: center;
  margin: 15px 10px;
}
</style>
