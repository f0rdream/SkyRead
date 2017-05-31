<template lang="html">
  <div class="cate-box">
    <recommend-card :recommendDetail="bookDetail"></recommend-card>
    <item-viewer></item-viewer>
  </div>
</template>

<script>
import ItemViewer from '@/components/ItemViewer'
import RecommendCard from '@/components/RecommendCard'

export default {
  components: {
    ItemViewer,
    RecommendCard
  },
  data () {
    return {
      isbn13: this.$route.params.isbn13 || '9787111251217',
      bookDetail: {
        isbn13: '',
        title: '',
        author: [],
        summary: '',
        average: '',
        pubdate: '',
        publisher: '',
        img_id: '',
        pages: '',
        tags: [],
        price: ''
      },
      imgId: ''
    }
  },
  mounted () {
    this.getBook()
  },
  methods: {
    getBook () {
      this.$http.get(`book/isbn/${this.isbn13}`).then((res) => {
        this.bookDetail = res.data
        this.imgId = res.data.img_id
      }).catch((err) => {
        console.log(err)
      })
    }
  }
}
</script>

<style lang="css">
</style>
