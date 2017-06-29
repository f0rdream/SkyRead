<template lang="html">
  <div class="title-container">
    <div class="title">他的书</div>
    <list-item v-for="item in bookList"  :itemInfo="item"></list-item>
  </div>
</template>

<script>
import ItemViewer from '@/components/ItemViewer'
import RecommendCard from '@/components/RecommendCard'
import ListItem from '@/components/ListItem'

export default {
  components: {
    ItemViewer,
    RecommendCard,
    ListItem
  },
  data () {
    return {
      personName: this.$route.params.personName,
      personIndex: this.$route.params.personIndex,
      bookList: []
    }
  },
  mounted () {
    this.getPersonBooks()
  },
  methods: {
    getPersonBooks () {
      this.$http.get(`/list/user_like/${this.personIndex}`).then(res => {
        this.bookList = res.data
      }).catch(err => console.warn(err))
    }
  }
}
</script>

<style lang="css" scoped>
</style>
