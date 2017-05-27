<template lang="html">
  <section class="viewer-box">
    <div class="title-box">
      <span class="title">
        新书速递
      </span>
      <span class="view-changer" @click="changeView" v-if="listable">
        {{ isList ? '网格视图' : '列表视图' }}
      </span>
    </div>
    <div class="viewer-block" v-if="!isList">
      <div v-for="item in currentItems" class="viewer-item">
        <img :src="item.img_id" class="item-img" @click="$router.push(`/home/bookdetail/${item.isbn13}`)">
        <p class="item-title">{{ item.title }}</p>
      </div>
    </div>
    <div class="list-block" v-else>
      <div v-for="item in currentItems" class="list-item vux-1px-b" @click="$router.push(`/home/bookdetail/${item.isbn13}`)">
        <p class="item-title">{{ item.title }}</p>
        <p class="item-info">作者：<span v-for="authorItem in item.author">{{ authorItem }}</span></p>
        <p class="item-info">出版信息：北京 中央书局   2011</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    items: Array,
    listable: {
      type: Boolean,
      default: true
    }
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
    },
    logU (event) {
      console.log(event.target)
    }
  }
}
</script>

<style lang="css">
.viewer-box {
  margin-top: .25rem;
  background-color: #fff;
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
