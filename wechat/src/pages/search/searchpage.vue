<template lang="html">
  <view-box>
    <div class="app-wrapper">
      <div class="img-part">
        <img src="/static/logo.png" class="logo">
      </div>
      <div class="search-part">
        <form class="search-container">
          <div class="search-box">
            <input type="search" class="search-input" placeholder="输入以搜索" v-model="searchString" @focus="searchFocus = true">
            <a class="i-btn i-btn-square search-btn" @click="search">
              <img src="/static/others/search_white.png" class="i-icon">
            </a>
          </div>
          <div class="history-box" v-show="searchFocus">
            <a class="history-item" v-for="item in searchHistory" @click="historyClick(item.title)">
              {{ item.title }}
            </a>
            <div class="history-bottom">
              <div class="left-part"></div>
              <div class="right-part">
                <a class="a-close" @click="searchFocus = false">关闭</a>
              </div>
            </div>
          </div>
        </form>
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
      searchFocus: false,
      searchMod: 0  // 0: history mod, 1: searching
    }
  },
  mounted () {
    this.getHistory()
  },
  methods: {
    getHistory () {
      this.$http.get('/history/search/').then(res => {
        for (let index in res.data) {
          if (index < 5) {
            this.searchHistory.push({title: res.data[index].key})
          }
        }
      }).catch(err => {
        console.log(err.response.data)
      })
    },
    historyClick (keyword) {
      this.searchString = keyword
      this.search()
    },
    search () {
      if (this.searchString) {
        this.$router.push(`/search/${this.searchString}`)
      }
    }
  }
}
</script>

<style lang="css" scoped>
.app-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
}
.img-part {
  flex-grow: 1;
  flex-shrink: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}
.logo {
  width: 100px;
}
.search-part {
  display: flex;
  flex-direction: column;
  flex-grow: 2;
  flex-shrink: 1;
  padding: 0 20px;
  outline: none;
}
.search-box {
  display: flex;
}
.search-input {
  flex: 1;
  border: 0;
  outline: none;
  padding-left: 15px;
  color: #444;
}
.search-btn {
  flex: 0;
}
.i-icon {
  height: 18px;
}
.i-btn-square {
  border-radius: 4px;
}

.history-box {
  border-top: 1px solid rgba(200, 200, 200, 0.4);
  background: #fff;
  padding-left: 15px;
  color: #555;
  font-size: 14px;
}
.history-item {
  display: block;
  padding: 4px 0;
  border-bottom: 1px solid rgba(200, 200, 200, 0.2);
}
.history-bottom {
  display: flex;
  height: 25px;
}
.history-bottom .left-part {
  flex-grow: 1;
}
.history-bottom .right-part {
  flex-grow: 0;
}
.a-close {
  display: inline-block;
  padding: 0 10px;
  border-left: 1px solid rgba(200, 200, 200, 0.5);
}
</style>
