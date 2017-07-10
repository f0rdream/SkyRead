<template>
  <div class="list-container" @click="changeSpread()">
    <div class="book-label" :class="isSpread ? 'vux-1px-tb' : 'vux-1px-t'" v-if="currentIsLabel">
      <span class="label-text">{{ currentLabel }}</span>
      <span class="label-btn">{{ isSpread ? '收起' : '展开'}}</span>
    </div>
    <div class="book-list vux-1px-b" v-for="book in currentbooks" v-show="isSpread" @click="$router.push(`/home/bookdetail/${book.isbn13}`)">
      <div class="left">
        <p class="book-title">{{ book.title}}</p>
        <p class="book-info">借阅时间: {{ book.borrow_time }}</p>
        <p class="book-info">归还时间: {{ book.return_time }}</p>
        <slot name="addition-info"></slot>
      </div>
      <div class="right">
        <slot name="right"></slot>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  props: {
    isLabel: {
      type: Boolean,
      default: true
    },
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
    },
    currentIsLabel () {
      return this.isLabel
    }
  },
  methods: {
    changeSpread () {
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
.book-list.vux-1px-b:last-child::after {
  border-bottom: none;
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
