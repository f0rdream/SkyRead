<template lang="html">
  <view-box class="list-container">
    <div class="title-container">
      <div class="title">根据标题</div>
      <list-item v-for="item in this.result.title_result"  :itemInfo="item"></list-item>
    </div>
    <div class="title-container">
      <div class="title">根据作者</div>
      <list-item v-for="item in this.result.author_result"  :itemInfo="item"></list-item>
    </div>
  </view-box>
</template>

<script>
import { ViewBox } from 'vux'
import ListItem from '@/components/ListItem'
export default {
  components: {
    ListItem,
    ViewBox
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
  border-bottom: 1px #333 solid;
}
</style>
