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
    <div class="viewer-block" v-if="!isList">
      <div v-for="item in currentItems" class="viewer-item">
        <img src="../images/s3083552.jpg"class="item-img">
        <p class="item-title">资治通鉴</p>
      </div>
    </div>
    <div class="list-block" v-else>
      <div v-for="item in currentItems" class="list-item vux-1px-b">
        <p class="item-title">《孔子》</p>
        <p class="item-info">作者：(中)孔丘    著</p>
        <p class="item-info">出版信息：北京 中央书局   2011</p>
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
.viewer-box {
  margin-top: .25rem;
  background-color: #fff;
}
.viewer-box .title-box {
  padding: .15rem .20rem .10rem .20rem;
}
.viewer-block {
  margin: 0 .20rem;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
}
.viewer-item {
  flex: 0 1 26%;
  text-align: center;
}
.viewer-item .item-img {
  width: 100%;
}
.viewer-item .item-title {
  font-size: 12px;
}
.list-block {
}
.list-item {
  padding: .10rem .20rem;
}
.list-item .item-title {
  font-size: 12px;
}
.list-item .item-info {
  color: #787878;
  font-size: 10px;
}
</style>
