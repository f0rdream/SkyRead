<template lang="html">
  <view-box class="app-wrapper">
    <search v-model="searchString" ref="search" @on-focus="onFocus" @on-cancel="onCancel" @on-submit="search"></search>
    <div class="history-title-container"  v-show="searchMod === 0">
      <p class="history-title">历史记录</p>
    </div>
    <div class="search-item-container" v-show="searchMod === 0">
      <div class="search-item" v-for="item in searchHistory" @click="historyClick(item.title)">
        <p class="search-item-text">{{ item.title }}</p>
      </div>
    </div>
    <bottom-bar :activeTab="1" slot="bottom"></bottom-bar>
  </view-box>
</template>

<script>
import { Search, ViewBox } from 'vux'
import BottomBar from '@/components/BottomBar'
export default {
  components: {
    BottomBar,
    Search,
    ViewBox
  },
  data () {
    return {
      searchString: '',
      searchHistory: [],
      searchMod: 0  // 0: history mod, 1: searching
    }
  },
  mounted () {
    this.getHistory()
  },
  methods: {
    getHistory () {
      this.$http.get('/history/search/').then(res => {
        for (let item of res.data) {
          this.searchHistory.push({title: item.key})
        }
      }).catch(err => {
        console.log(err)
      })
    },
    historyClick (keyword) {
      this.$refs.search.setFocus()
      this.searchString = keyword
      this.search()
    },
    onFocus () {
      this.searchMod = 1
    },
    onCancel () {
      this.searchMod = 0
    },
    search () {
      this.$router.push(`/search/${this.searchString}`)
    }
  }
}
</script>

<style lang="css" scoped>
.history-title-container {
  background-color: #fff;
  border-bottom: 1px solid #D9D9D9;
}
.history-title {
  padding-left: 10px;
  color: #555;
  font-size: 14px;
}
.search-item-container {
  background-color: #fff;
}
.search-item {
  font-size: 14px;
  margin-left: 15px;
  padding: 8px 15px 8px 0;
}
.search-item:not(:first-child) {
  border-top: 1px solid #D9D9D9;
}
.search-item-text {
  /*font-size: 17px;*/
}
</style>
