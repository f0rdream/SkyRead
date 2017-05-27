<template lang="html">
  <div class="search-part">
    <div class="before-search-box">
      <div class="history-part">
        <div class="history-item" v-for="historyItem in historyItems">
          {{historyItem}}
        </div>
      </div>
      <recommend-card :items="recommendItems"></recommend-card>
    </div>
  </div>
</template>

<script>
import RecommendCardMulti from './RecommendCardMulti'
export default {
  components: {
    RecommendCardMulti
  },
  data () {
    return {
      historyItems: ['1', '1', '1', '1', '1'],
      recommendItems: ['1', '1', '1', '1', '1']
    }
  }
}
</script>

<style lang="css" scoped>
</style>
