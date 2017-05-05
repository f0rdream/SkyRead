<template>
  <div class="list-container" @click="changeSpread()">
    <div class="book-label" :class="isSpread ? 'vux-1px-tb' : 'vux-1px-t'">
      <span class="label-text">{{ currentLabel }}</span>
      <span class="label-btn">{{ isSpread ? '收起' : '展开'}}</span>
    </div>
    <div class="book-list vux-1px-b" v-for="book in currentbooks" v-show="isSpread">
      <div class="left">
        <p class="book-title">《孔子》</p>
        <p class="book-info">作者：(中)孔丘    著</p>
        <p class="book-info">出版信息：北京 中央书局   2011</p>
        <p class="book-info">取书日期：2017-5-14</p>
        <p class="book-info">取书地点：信息学部图书馆</p>
      </div>
      <div class="right">
        <router-link to="/detail" class="book-detail">详情</router-link>
        <span class="book-del">删除</span>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: {
    labelText: String,
    books: Array
  },
  data () {
    return {
      isSpread: false
    }
  },
  mounted () {
  },
  computed: {
    currentLabel () {
      return this.labelText
    },
    currentbooks () {
      return this.books
    }
  },
  methods: {
    changeSpread () {
      console.log('lala')
      this.isSpread = !this.isSpread
    }
  }
}
</script>

<style>
.list-container {
  background-color: #ffffff;
}
.book-label, .book-list {
  display: flex;
  justify-content: space-between;
}
.book-label {
  padding: 8px 15px;
}
.book-list {
  margin: 8px 20px;
  padding: 0 5px 5px 5px;
}
.book-label .label-text {
  line-height: 27px;
}
.book-label .label-btn {
  color: #858585;
  font-size: 12px;
  line-height: 27px;
}
.book-list .book-title {
  font-size: 12px;
}
.book-list .book-info {
  color: #787878;
  font-size: 10px;
}
.book-list .book-detail, .book-list .book-del {
  font-size: 10px;
}
.book-list .right {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
