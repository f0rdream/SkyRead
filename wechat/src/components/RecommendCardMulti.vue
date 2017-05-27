<template lang="html">
  <div class="recommend-card">
    <div class="card-title">
      <span class="title-content">猜你喜欢</span>
      <span class="button">换一批</span>
    </div>
    <div class="card-content">
      <div class="content-item" v-for="item in currentItems">
        <span class="item-name">《嫌疑人X的献身》  作者：[日]东野圭吾</span>
        <span class="item-score">9.0分</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    items: Array
  },
  computed: {
    currentItems () {
      return this.items
    }
  }
}
</script>

<style lang="css">
</style>
