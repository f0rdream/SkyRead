<template lang="html">
  <clickable-list :isLabel="false"></clickable-list>
</template>

<script>
import ClickableList from '@/components/ClickableList'

export default {
  components: {
    ClickableList
  },
  data () {
    return {
      bookList: []
    }
  },
  methods: {
    getData () {
      this.$http.get('library/borrow/').then(res => {
        this.bookList = res.data
      }).catch(err => {
        console.log(err)
      })
    }
  }
}
</script>

<style lang="css" scoped>
</style>
