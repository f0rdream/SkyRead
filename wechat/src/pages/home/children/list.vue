<template lang="html">
  <div class="title-container">
    <div class="title">
      <p class="title-string">{{ itemId }}</p>
    </div>
    <list-item v-for="item in itemList"  :itemInfo="item" :key="item.isbn13"></list-item>
    <infinite-loading :on-infinite="onInfinite" ref="infiniteLoading"></infinite-loading>
  </div>
</template>

<script>
import ItemViewer from '@/components/ItemViewer'
import RecommendCard from '@/components/RecommendCard'
import ListItem from '@/components/ListItem'
import InfiniteLoading from 'vue-infinite-loading'

export default {
  components: {
    ItemViewer,
    RecommendCard,
    ListItem,
    InfiniteLoading
  },
  data () {
    return {
      kind: this.$route.params.kind,
      itemId: this.$route.params.itemId,
      itemList: [],
      pageNum: 0
    }
  },
  mounted () {
  },
  methods: {
    onInfinite () {
      this.pageNum += 1
      if (this.kind === 'tag') {
        this.$http.get(`/list/tag/${this.pageNum}/?key=${this.itemId}`).then(res => {
          this.itemList = this.itemList.concat(res.data)
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
        }).catch((err) => {
          console.error(err)
        })
      } else if (this.kind === 'author') {
        this.$http.get(`/list/author/${this.pageNum}/?key=${this.itemId}`).then(res => {
          this.itemList = this.itemList.concat(res.data)
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
        }).catch((err) => {
          console.error(err)
        })
      }
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
