<template lang="html">
  <div class="page-wrapper">
    <tab v-model="selectedIndex" bar-active-color="#2bc6b9" active-color="#2bc6b9">
      <tab-item v-for="item in tabItems" @on-item-click="$router.replace(item.src)" :key="item.src">{{item.label}}</tab-item>
    </tab>
    <div class="item-container" v-for="item in items" :key="item.id">
      <div class="left"></div>
      <div class="right">
        <p class="item-title">{{ item.title }}</p>
        <p class="item-info">{{ item.comment }}</p>
      </div>
    </div>
    <infinite-loading :on-infinite="onInfinite" ref="infiniteLoading"></infinite-loading>
  </div>
</template>

<script>
import { Tab, TabItem } from 'vux'
import InfiniteLoading from 'vue-infinite-loading'

export default {
  components: {
    Tab,
    TabItem,
    InfiniteLoading
  },
  data () {
    return {
      tabItems: [
        { src: '/bookshelf/scaned', label: '已扫码' },
        { src: '/bookshelf/ordered', label: '已预订' },
        { src: '/bookshelf/renting', label: '正在借阅' }
      ],
      pageNum: 1,
      items: [],
      orderType: ['star', 'time'],
      selectedIndex: 0
    }
  },
  watch: {
    selectedIndex (newValue) {
      switch (newValue) {
        case 0:
          this.pageNum = 1
          this.items = []
          break
        case 1:
          this.pageNum = 1
          this.items = []
          break
      }
    }
  },
  methods: {
    getItems () {
      this.$http.get(`/accounts/cycle/${this.pageNum}/?order=star`).then(res => {
        this.items = res.data
      }).catch(err => console.log(err.response.data))
    },
    onInfinite () {
      this.$http.get(`/accounts/cycle/${this.pageNum}/?order=${this.orderType[this.selectedIndex]}`).then((res) => {
        if (res.data.length !== 0) {
          this.items = this.items.concat(res.data)
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
          this.pageNum += 1
        }
      }).catch((err) => {
        console.error(err)
      })
    }
  }
}
</script>

<style lang="css" scoped>
</style>
