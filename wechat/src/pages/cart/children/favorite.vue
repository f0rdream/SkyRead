<template lang="html">
  <div class="children-container">
    <book-cell v-for="(book,index) in bookList" :key="book.id">
      <!-- <input slot="book-checker" type="checkbox" :value="book.id" v-model="checkedCells"> -->
      <p slot="book-title" class="book-title">{{ book.short_info.title }}</p>
      <p slot="book-info" class="book-info">作者: <span v-for="author in book.short_info.author">{{ author }}</span></p>
      <p slot="book-info" class="book-info">评分: {{ book.short_info.average}}</p>
      <button class="i-btn multi-btn" slot="right" @click="bookClick(book.short_info.isbn13)">书籍详情</button>
      <button class="i-btn multi-btn" slot="right" @click="delFavorite(book.id)">删除</button>
    </book-cell>
    <!-- <x-button @click.native="genQR(checkedCells)" :disabled="allQRAvailble">批量删除</x-button> -->
  </div>
</template>

<script>
import BookCell from '@/components/BookCell'
import { mapActions, mapState } from 'vuex'
// import ClickableList from '@/components/ClickableList'

export default {
  components: {
    BookCell
  },
  data () {
    return {
      // checkedCells: []
    }
  },
  computed: {
    // allQRAvailble () {
    //   if (this.checkedCells.length !== 0) {
    //     return false
    //   }
    //   return true
    // },
    ...mapState({
      'bookList': 'favorite'
    })
  },
  mounted () {
    this.getFavorite()
  },
  methods: {
    ...mapActions([
      'getFavorite',
      'delFavorite'
    ]),
    bookClick (isbn13) {
      this.$router.push(`/home/bookdetail/${isbn13}`)
    }
  }
}
</script>

<style lang="css" scoped>
</style>
