<template>
  <div class="component-container">
    <div class="book-card card">
      <div class="book-body">
        <div class="left">
          <img :src="bookDetail.imgSrc" class="book-img">
        </div>
        <div class="right">
          <p class="body-title"> {{ bookDetail.title }}</p>
          <p class="body-info author">作者：<span v-for="item in bookDetail.author">{{ item }}</span></p>
          <p class="body-info">页数：{{ bookDetail.pages }}</p>
          <p class="body-info">出版社：{{ bookDetail.publisher }}</p>
          <p class="body-info">出版时间：{{ bookDetail.pubdate }}</p>
        </div>
      </div>
    </div>
    <div class="total-card card">
      <div>共{{basicInfo.amount}}家店铺</div>
      <div>最高价: {{basicInfo.max}}</div>
      <div>最低价: {{basicInfo.min}}</div>
    </div>
    <div class="price-card card" v-for="item in priceList">
      <div class="price-title">{{ item.source_name }}</div>
      <div class="price-detail">
        <div class="price-box">
          价格: <span class="price-span">{{ item.price }}</span>
        </div>
        <div class="opt-box">
          <button class="i-btn buy-btn">前往购买</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { XImg } from 'vux'
export default {
  components: {
    XImg
  },
  data () {
    return {
      isbn13: this.$route.params.isbn13,
      bookDetail: {
        isbn13: '',
        title: '',
        author: [],
        summary: '',
        average: '',
        pubdate: '',
        publisher: '',
        imgSrc: '',
        img_id: '',
        pages: '',
        tags: [],
        price: ''
      },
      priceList: []
    }
  },
  computed: {
    basicInfo () {
      if (this.priceList.length === 0) {
        return {amount: 0, max: 0, min: 0}
      }
      let arr = []
      for (let i in this.priceList) {
        arr.push(this.priceList[i].price.split('￥')[1])
      }
      let max = Math.max.apply(Math, arr)
      let min = Math.min.apply(Math, arr)
      return {amount: arr.length, max, min}
    }
  },
  mounted () {
    this.getBook()
    this.getPrice()
  },
  methods: {
    getBook () {
      this.$http.get(`book/isbn/${this.isbn13}`).then((res) => {
        this.bookDetail = res.data
        this.bookDetail.imgSrc = 'https://img3.doubanio.com/lpic/' + res.data.img_id
      }).catch((err) => {
        console.log(err.response.data)
      })
    },
    getPrice () {
      this.$http.get(`book/price/?isbn13=${this.isbn13}`).then((res) => {
        if (res.data !== 404) {
          this.priceList = res.data
        }
      }).catch((err) => {
        console.log(err.response.data)
      })
    }
  }
}
</script>

<style lang="css" scoped>
.component-container {
  color: #5d5d5d;
}
.card {
  margin: .08rem .16rem;
  background-color: #fff;
}
.book-body {
  display: flex;
  padding: .15rem .05rem;
}
.book-body>.left {
  flex: 0 0 35%;
  text-align: center;
}
.book-img {
  width: 80%;
}
.book-body>.right {
  flex: 1 1 auto;
  padding-left: .05rem;
}
.body-title {
  font-size: 16px;
  margin-bottom: .10rem;
}
.body-info {
  font-size: 13px;
}
.body-info.author {
  white-space: normal;
}
.total-card {
  display: flex;
  padding: .10rem .05rem;
  justify-content: space-around;
  font-size: 14px;
}
.price-card {
  padding: .10rem .15rem;
  font-size: 14px;
}
.price-card>div {
  padding-left: .08rem;
}
.price-title {
  border-bottom: 1px solid #dfdfdf;
}
.price-detail {
  display: flex;
  padding-top: .08rem;
  justify-content: space-between;
  align-items: center;
}
.price-span {
  color: #f38c39;
}
.buy-btn {
  background-color: #f87d3a;
}
</style>
