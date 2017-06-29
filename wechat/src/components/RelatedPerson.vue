<template lang="html">
  <section class="viewer-box">
    <div class="title-box">
      <span class="title">
        猜你喜欢
      </span>
      <span class="view-changer" @click="switchItem">
        换一换
      </span>
    </div>
    <div class="viewer-block">
      <div v-for="(item, index) in currentItems" :key="item.isbn13" class="viewer-item">
        <img :src="getImg(index)" class="item-img" @click="$router.push(`/relatedperson/${index}/${item}`)">
        <p class="item-title">{{ item.title }}</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  data () {
    return {
      flag: 0, // Flag to control the switch button
      totalItems: [],
      currentItems: []
    }
  },
  mounted () {
    this.getPeople()
  },
  methods: {
    getPeople () {
      this.$http.get('/list/user_like/').then(res => {
        this.totalItems = res.data.user_list
        this.currentItems = this.totalItems.slice(0, 3)
      }).catch(err => console.warn('Err: ' + err))
    },
    switchItem () {
      const amount = 6
      const flagMax = parseInt(this.totalItems.length / amount)
      if (this.flag < flagMax - 1) {
        this.flag += 1
      } else {
        this.flag = 0
      }
      this.currentItems = this.totalItems.slice(this.flag * amount, this.flag * amount + 6)
    },
    getImg (index) {}
  }
}
</script>

<style lang="css" scoped>
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
</style>
