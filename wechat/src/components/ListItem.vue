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
          <p class="item-info">作者：<span v-for="author in bookInfo.author" :key="bookInfo.isbn13">{{author}} </span></p>
          <p class="item-info">出版信息：{{ bookInfo.publisher }}</p>
          <p class="item-info">评分：{{ bookInfo.average }}</p>
        </div>
        <div class="item-info-right">
          <button class="i-btn" mini @click="addFavorite(bookInfo.isbn13)">收藏</button>
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
      'addFavorite'
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
  flex-grow: 0;
  flex-shrink: 0;
  flex-basis: 25%;
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
}
.item-info-left {
  flex-grow: 1;
  padding-right: 10px;
}
.item-info-right {
  flex-grow: 0;
  flex-shrink: 0;
  padding-right: 15px;
}
</style>
