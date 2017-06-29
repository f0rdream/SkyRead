<template lang="html">
  <div class="item-container">
    <div class="left-part" @click="bookClick">
      <img class="book-img" :src="`https://img3.doubanio.com/lpic/${this.bookInfo.img_id}`">
    </div>
    <div class="right-part">
      <p class="item-title" @click="bookClick">
        {{ bookInfo.title }}
      </p>
      <div class="item-info-container">
        <div class="item-info-left" @click="bookClick">
          <p class="item-info">作者：<span v-for="author in bookInfo.author" :key="bookInfo.isbn13">{{author}}</span></p>
          <p class="item-info">出版信息：{{ bookInfo.publisher }}</p>
          <p class="item-info">评分：{{ bookInfo.average }}</p>
          <p class="item-info">价格：{{ bookInfo.price }}</p>
        </div>
        <div class="item-info-right">
          <x-button type="primary" mini @click.native="addFavroite(bookInfo.isbn13)">收藏</x-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { XButton } from 'vux'
import { mapActions } from 'vuex'

export default {
  components: {
    XButton
  },
  props: {
    itemInfo: Object
  },
  data () {
    return {
      bookInfo: this.itemInfo
    }
  },
  methods: {
    ...mapActions([
      'addFavroite'
    ]),
    bookClick () {
      this.$router.push(`/home/bookdetail/${this.bookInfo.isbn13}`)
    }
  }
}
</script>

<style lang="css" scoped>
.item-container {
  display: flex;
  background-color: #fff;
}
.left-part {
  width: 25%;
  min-width: 25%;
  padding: 15px 15px;
}
.book-img {
  width: 100%;
}
.right-part {
  display: flex;
  flex-direction: column;
  justify-content: center;
  flex-grow: 1;
}
.item-title {
  font-size: 15px;
  color: #393939;
  font-weight: 500;
}
.item-info {
  line-height: 1.5;
  font-size: 12px;
  color: #787878;
}
.item-info-container {
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.item-info-right {
  margin: 15px;
}
</style>
