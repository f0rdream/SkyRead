<template>
  <div class="detail-box">
    <div class="book-card">
      <div class="book-body">
        <div class="left">
          <img :src="bookDetail.imgSrc" class="book-img">
          <p class="body-title ellipsis">{{ bookDetail.title }}</p>
          <div class="opt-box">
            <!--  TODO  添加收藏的mutation -->
            <router-link to="">收藏</router-link>
          </div>
        </div>
        <div class="right">
          <p class="body-info">作者：{{ bookDetail.author }}</p>
          <p class="body-info">作者简介：{{ bookDetail.author_intro }}</p>
          <p class="body-info">出版社：{{ bookDetail.publisher }}</p>
          <p class="body-info">出版时间：{{ bookDetail.pubdate }}</p>
          <p class="body-info">价格：{{ bookDetail.price }}</p>
          <p class="body-info">ISBN：{{ bookDetail.isbn13 }}</p>
          <p class="body-info">页数：{{ bookDetail.pages }}页</p>
          <p class="body-info">标签： <router-link v-for="item in bookDetail.tags" to="" :key="bookDetail.tags">{{ item }} </router-link></p>
          <div class="times-box">
            <div class="times-info">
              <p>16524人</p>
              <p>读过</p>
            </div>
            <div class="times-info">
              <p>16524人</p>
              <p>收藏</p>
            </div>
            <div class="times-info">
              <p class="times-score">{{ bookDetail.average }}</p>
              <p>豆瓣评分</p>
            </div>
          </div>
        </div>
      </div>
      <div class="book-description book-part">
        <p class="part-title">内容简介</p>
        <p class="part-body">{{ bookDetail.summary }}</p>
      </div>
      <div class="book-index book-part">
        <p class="part-title">内容简介</p>
        <p class="part-body">一行共有三十个字，该字号为二十像素，内容简介字号二十八像素，测试</p>
      </div>
    </div>
    <div class="store-box">
      <p class="store-title">馆藏信息</p>
      <table class="store-table">
        <tr class="table-head">
          <th>书籍定位</th>
          <th>状态</th>
          <th>应还日期</th>
          <th>预订</th>
        </tr>
        <tr class="table-item">
          <td>3楼C区15架</td>
          <td>在架上</td>
          <td>2015-1-1</td>
          <td>添加</td>
        </tr>
      </table>
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
      isbn13: this.$route.params.isbn13 || '9787111251217',
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
      }
    }
  },
  mounted () {
    this.getBook()
  },
  methods: {
    getBook () {
      this.$http.get(`book/isbn/${this.isbn13}`).then((res) => {
        this.bookDetail = res.data
        this.bookDetail.imgSrc = 'https://img3.doubanio.com/lpic/' + res.data.img_id
      }).catch((err) => {
        console.log(err)
      })
    }
  }
}
</script>

<style lang="css" scoped>
.detail-box>div {
  background-color: #fbfbfb;
}
.book-body {
  display: flex;
  flex-flow: row nowrap;
  padding: .05rem .15rem ;
  justify-content: space-between;
}
.book-body .left {
  text-align: center;
  width: 1.3rem;
  flex: 1 1 auto;
  height: 100%;
}
.book-body .left .book-img {
  width: 100%;
}
.book-body .left .body-title {
  font-size: 14px;
}
.book-body .left .opt-box {
  font-size: 12px;
}
.book-part {
  margin: .05rem 0;
  padding: .10rem .15rem;
  border-top: 1px solid #333;
}
.book-part .part-title {
  font-size: 14px;
}
.book-part .part-body {
  font-size: 10px;
}

.book-body .right {
  font-size: 10px;
  max-width: 2.4rem;
  flex: 1.5 1 auto;
  margin: 0 0.10rem;
}
.book-body .right .body-info {
  margin: .08rem 0;
}
.book-body .times-box {
  display: flex;
  justify-content: space-between;
}
.book-body .times-box .times-info {
  text-align: center;
}
.book-body .times-box .times-info:nth-child(2) {
  border-left: 1px solid #000;
  border-right: 1px solid #000;
  padding: 0 .15rem;
}
.book-body .times-box .times-score{
  color: #ff8019;
}

.store-box {
  margin: .15rem 0;
  padding: 0 .15rem;
}
.store-table {
  width: 100%;
  text-align: center;
}
</style>
