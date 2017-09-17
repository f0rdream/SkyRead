<template lang="html">
  <view-box class="list-container">
    <div class="title-container">
      <list-item v-for="item in this.result.title_result"  :itemInfo="item" :key="item.isbn13"></list-item>
    </div>
    <bottom-bar :activeTab="1" slot="bottom"></bottom-bar>
  </view-box>
</template>

<script>
import { ViewBox } from 'vux'
import ListItem from '@/components/ListItem'
import BottomBar from '@/components/BottomBar'
import ISelect from '@/components/Select'

export default {
  components: {
    ListItem,
    ViewBox,
    BottomBar,
    ISelect
  },
  data () {
    return {
      keyword: this.$route.params.keyword,
      result: {},
      typeIndex: 0,
      bookIndex: 0,
      typeItems: [
        {title: '根据标题'}, {title: '根据作者'}, {title: '根据作者'}
      ],
      bookItems: [
        {title: '普通书'}, {title: '电子书'}
      ]
    }
  },
  mounted () {
    this.getResult()
  },
  watch: {
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
.select-tab {
  width: 49%;
}
</style>
