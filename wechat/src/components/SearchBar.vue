<template>
  <search :placeholder="currentPlaceHolder"></search>
</template>

<script>

import { Search } from 'vux'
export default {
  props: {
    placeholder: String
  },
  components: {
    Search
  },
  data () {
    return {
      currentPlaceHolder: this.placeholder
    }
  },
  methods () {}
}
</script>
<style>
</style>
