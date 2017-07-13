<template lang="html">
  <div class="title-container">
    <div class="title">
      <p class="title-string">你附近的书</p>
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
      itemList: []
    }
  },
  mounted () {
    this.getList()
  },
  methods: {
    getList () {
      let num = Math.ceil(Math.random() * 10) + 5
      this.$http.get(`/book/guide/3/${num}`).then(res => {
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
