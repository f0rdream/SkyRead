<template>
  <div class="detail-box">
    <div class="book-card ">
      <div class="book-body-container">
        <div class="book-background" :style="{backgroundImage: `url(${bookDetail.imgSrc})`}"></div>
        <div class="book-body">
          <div class="left">
            <img :src="bookDetail.imgSrc" class="book-img">
          </div>
          <div class="right">
            <p class="body-title ellipsis">{{ bookDetail.title }}</p>
            <p class="body-info ellipsis">标签： <router-link v-for="item in bookDetail.tags" :to="`/home/list/tag/${item}`" :key="bookDetail.tags" class="info-link">{{ item }}, </router-link></p>
            <p class="body-info ellipsis">作者：<router-link v-for="item in bookDetail.author" class="info-link" :to="`/home/list/author/${item}`" :key="bookDetail.author">{{item}}, </router-link></p>
            <p class="body-info">出版社：{{ bookDetail.publisher }}</p>
            <p class="body-info">出版时间：{{ bookDetail.pubdate }}</p>
            <p class="body-info">ISBN：{{ bookDetail.isbn13 }}</p>
            <p class="body-info">豆瓣评分：{{ bookDetail.average }}</p>
          </div>
        </div>
        <div class="book-opt">
          <div class="left"></div>
          <div class="right">
            <a class="i-btn-blank"><img src="/static/others/collect.png" class="i-btn-icon" @click="clickFavor">收藏</a>
            <a class="i-btn-blank"><img src="/static/others/comment.png" class="i-btn-icon" @click="comment">评论</a>
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
import { mapActions } from 'vuex'
export default {
  components: {
    XImg
  },
  data () {
    return {
      isbn13: this.$route.params.isbn13 || '9787111251217',
      bookDetail: {}
    }
  },
  mounted () {
    this.getBook()
  },
  methods: {
    ...mapActions({
      addFavorite: 'addFavorite'
    }),
    getBook () {
      this.$http.get(`book/isbn/${this.isbn13}`).then((res) => {
        let tagsMax = []
        let authorMax = []
        for (let index in res.data.tags) {
          if (index < 5) {
            tagsMax.push(res.data.tags[index])
          }
        }
        for (let index in res.data.author) {
          if (index < 5) {
            authorMax.push(res.data.author[index])
          }
        }
        this.bookDetail = {...res.data, ...{ tags: tagsMax, author: authorMax }}
        this.bookDetail.imgSrc = 'https://img3.doubanio.com/lpic/' + res.data.img_id
      }).catch((err) => {
        console.log(err)
      })
    },
    comment () {
      console.log('comment')
    },
    clickFavor () {
      this.addFavorite(this.bookDetail.isbn13)
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
  padding: .05rem .15rem ;
}
.left {
  text-align: center;
  flex: 0 0 35%;
  height: 100%;
}
.book-img {
  width: 90%;
  border: 3px #fff solid;
  border-radius: 2px;
  position: relative;
  top: 35px;
}

.right {
  font-size: 11px;
  flex: 0 1 auto;
  padding: 0 0.10rem;
  overflow: hidden;
}
.book-part {
  position: relative;
  margin: .05rem 0;
  padding: .10rem .15rem;
  background-color: #fff;
  z-index: 100;
}
.book-part .part-body {
  font-size: 10px;
}

.body-info {
  margin: .04rem 0;
}
.times-box {
  display: flex;
  justify-content: space-between;
}
.times-info {
  text-align: center;
}
.times-info:nth-child(2) {
  border-left: 1px solid #000;
  border-right: 1px solid #000;
  padding: 0 .15rem;
}
.times-score{
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

.book-background {
  position: relative;
  height: 180px;
  z-index: 0;
  filter: blur(10px);
}
.book-body {
  position: relative;
  margin-top: -180px;
  color: #cecece;
  z-index: 100;
  padding-top: 20px;
  background-color: rgba(50, 50, 50, 0.6)
}

.body-title {
  font-size: 16px;
  font-weight: 600;
}
.info-link {
  color: #2bc5bc;
  text-decoration: underline;
}
.book-opt {
  display: flex;
  padding: 6px 10px;
  background-color: #fff;
}

.book-opt .i-btn-blank {
  margin: 0 5px;
  vertical-align: baseline;
}
.i-btn-icon {
  height: 12px;
  vertical-align: baseline;
  padding-right: 4px;
}
</style>
