<template lang="html">
  <div class="title-container">
    <div class="title">
      <p class="title-string">{{person}} 的书</p>
    </div>
    <list-item v-for="item in itemList"  :itemInfo="item" :key="item.isbn13"></list-item>
  </div>
</template>

<script>
import ListItem from '@/components/ListItem'
export default {
  components: {
    ListItem
  },
  data () {
    return {
      itemList: [],
      person: this.$route.params.item,
      index: this.$route.params.index
    }
  },
  mounted () {
    this.getList()
  },
  methods: {
    getList () {
      this.$http.get(`/list/user_like/${this.index}/`).then(res => {
        this.itemList = res.data
      }).catch(err => console.log(err.response.data))
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
