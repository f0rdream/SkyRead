<template lang="html">
  <view-box class="list-container">
    <div class="title-container">
      <div class="title">
        <p class="title-string">根据标题</p>
      </div>
      <list-item v-for="item in this.result.title_result"  :itemInfo="item" :key="item.isbn13"></list-item>
    </div>
    <div class="title-container">
      <div class="title">
        <p class="title-string">根据作者</p>
      </div>
      <list-item v-for="item in this.result.author_result"  :itemInfo="item" :key="item.isbn13"></list-item>
    </div>
    <bottom-bar :activeTab="1" slot="bottom"></bottom-bar>
  </view-box>
</template>

<script>
import { ViewBox } from 'vux'
import ListItem from '@/components/ListItem'
import BottomBar from '@/components/BottomBar'

export default {
  components: {
    ListItem,
    ViewBox,
    BottomBar
  },
  data () {
    return {
      keyword: this.$route.params.keyword,
      result: {}
    }
  },
  mounted () {
    this.getResult()
  },
  methods: {
    getResult () {
      this.$http.get(`/book/search/?key=${this.keyword}`).then(res => {
        this.result = res.data
      }).catch(err => {
        console.log('err:' + err)
      })
    }
  }
}
</script>

<style lang="css" scoped>
.title {
  border-bottom: 1px solid rgba(200, 200, 200, 0.5);
}
.title-string {
  padding-left: 15px;
  font-size: 14px;
  color: #919191;
}
</style>
