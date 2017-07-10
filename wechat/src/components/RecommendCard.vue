<template lang="html">
  <section class="viewer-box">
    <div class="title-box">
      <div class="left-part">
        <span class="title">
          猜你喜欢
        </span>
      </div>
      <div class="right-part">
        <span class="view-changer" @click="changeView" v-if="listable">
          {{ isList ? '网格视图' : '列表视图' }}
        </span>
        <span class="item-changer" @click="switchItem">
          换一批
        </span>
      </div>
    </div>
    <div class="viewer-block" v-if="!isList">
      <div v-for="item in currentItems" :key="item.isbn13" class="viewer-item">
        <img :src="getImg(item.img_id)" class="item-img" @click="$router.push(`/home/bookdetail/${item.isbn13}`)">
        <p class="item-title">{{ item.title }}</p>
      </div>
    </div>
    <div class="list-block" v-else>
      <div v-for="item in currentItems" class="list-item vux-1px-b" @click="$router.push(`/home/bookdetail/${item.isbn13}`)" :key="item.isbn13">
        <p class="item-title">{{ item.title }}</p>
        <p class="item-info">作者：<span v-for="authorItem in item.author">{{ authorItem }}</span></p>
        <p class="item-info">评分: {{ item.average }}</p>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  props: {
    bookItems: Array,
    listable: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      isList: false,
      flag: 0, // Flag to control the switch button
      // totalBooks: this.bookItems,
      currentItems: []
    }
  },
  mounted () {
  },
  computed: {
    totalBooks () {
      return this.bookItems
    }
  },
  watch: {
    bookItems: function () {
      this.currentItems = this.totalBooks.slice(0, 6)
    }
  },
  methods: {
    changeView () {
      this.isList = !this.isList
    },
    getImg (imgId) {
      return `https://img3.doubanio.com/lpic/${imgId}`
    },
    switchItem () {
      const amount = 6
      const flagMax = parseInt(this.totalBooks.length / amount)
      if (this.flag < flagMax - 1) {
        this.flag += 1
      } else {
        this.flag = 0
      }
      this.currentItems = this.totalBooks.slice(this.flag * amount, this.flag * amount + 6)
    }
  }
}
</script>

<style lang="css" scoped>
.viewer-box {
  margin-top: .25rem;
  background-color: #fff;
  padding-bottom: .10rem;
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
.title-box {
  display: flex;
  padding: 10px 15px;
  justify-content: space-between;
}
.title {
  padding: 2px 5px;
  border-bottom: 2px #2bc1c8 solid;
  font-weight: 600;
  color: #5f5f5f;
}
.view-changer, .item-changer {
  padding: 2px 5px;
  font-size: 14px;
  color: #5f5f5f;
}
</style>
