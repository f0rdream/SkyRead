<template lang="html">
  <div class="title-container">
    <div class="title">
      <p class="title-string">{{ bookTypes[typeId].type }}</p>
    </div>
    <list-item v-for="item in typeList"  :itemInfo="item" :key="item.isbn13"></list-item>
    <infinite-loading :on-infinite="onInfinite" ref="infiniteLoading"></infinite-loading>
  </div>
</template>

<script>
import ItemViewer from '@/components/ItemViewer'
import RecommendCard from '@/components/RecommendCard'
import ListItem from '@/components/ListItem'
import InfiniteLoading from 'vue-infinite-loading'
import { bookTypes } from '@/config/data'

export default {
  components: {
    ItemViewer,
    RecommendCard,
    ListItem,
    InfiniteLoading
  },
  data () {
    return {
      typeId: this.$route.params.typeid,
      typeList: [],
      pageNum: 0,
      bookTypes: bookTypes
    }
  },
  mounted () {
  },
  methods: {
    onInfinite () {
      this.pageNum += 1
      this.$http.get(`book/guide/${this.typeId}/${this.pageNum}`).then((res) => {
        this.typeList = this.typeList.concat(res.data)
        this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
      }).catch((err) => {
        console.error(err)
      })
    }
  }
}
</script>

<style lang="css" scoped>
.title {
  background-color: #fff;
  border-bottom: 1px solid rgba(200, 200, 200, 0.5);
}
.title-string {
  padding-left: 15px;
  font-size: 14px;
  color: #919191;
}
</style>
