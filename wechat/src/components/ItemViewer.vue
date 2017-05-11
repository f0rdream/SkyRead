<template lang="html">
  <section class="viewer-box">
    <div class="title-box">
      <span class="title">
        新书速递
      </span>
      <span class="view-changer" @click="changeView">
        {{ isList ? '网格视图' : '列表视图' }}
      </span>
    </div>
    <div class="viewer-block">
      <div v-for="item in currentItems" class="viewer-item">
        <img src="../images/s3083552.jpg" height="128" width="88">
        <span>资治通鉴</span>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    items: Array
  },
  data () {
    return {
      isList: false
    }
  },
  computed: {
    currentItems () {
      return this.items
    }
  },
  methods: {
    changeView () {
      this.isList = !this.isList
    }
  }
}
</script>

<style lang="css">
.viewer-block {
  display: flex;
}
.viewer-item {
  width: 33%;
}
</style>
