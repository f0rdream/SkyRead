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
            <a class="i-btn-blank" @click="clickFavor"><img src="/static/others/collect.png" class="i-btn-icon">收藏</a>
            <a class="i-btn-blank" @click="comment"><img src="/static/others/comment.png" class="i-btn-icon">评论</a>
          </div>
        </div>
      </div>
      <div class="book-description book-part">
        <p class="part-title">
          <span>内容简介</span>
          <img class="more-icon" :src="isContentMuch ? '/static/others/unfold.png' : '/static/others/fold.png'" @click="isContentMuch = !isContentMuch"></img>
        </p>
        <p class="part-body" v-show="!isContentMuch">{{ bookDetail.summary }}</p>
      </div>
      <div class="book-index book-part">
        <p class="part-title">
          <span>书籍简介</span>
          <img class="more-icon" :src="isIndexMuch ? '/static/others/unfold.png' : '/static/others/fold.png'" @click="isIndexMuch = !isIndexMuch"></img>
        </p>
        <div v-html="bookDetail.catalog" v-show="!isIndexMuch" class="part-body"></div>
      </div>
    </div>
    <div class="store-box">
      <p class="part-title">
        <span>馆藏信息</span>
        <img class="more-icon" :src="isTableMuch ? '/static/others/unfold.png' : '/static/others/fold.png'" @click="isTableMuch = !isTableMuch"></img>
      </p>
      <table class="store-table" v-show="!isTableMuch">
        <tr class="table-head">
          <th>书籍定位</th>
          <th>状态</th>
          <th>应还日期</th>
          <th>预订</th>
        </tr>
        <tr class="table-item" v-for="item in storeInfo">
          <td>{{ item.location }}</td>
          <td>{{ item.state }}</td>
          <td>{{ item.back_time }}</td>
          <td><a class="info-link" @click="orderBook(item.id, item.isbn13, item.state)">预定</a></td>
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
      bookDetail: {},
      isContentMuch: false,
      isIndexMuch: true,
      isTableMuch: true,
      storeInfo: {}
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
        this.getStoreInfo()
      }).catch((err) => {
        console.log(err)
      })
    },
    comment () {
      this.$router.push(`/home/comment/${this.bookDetail.isbn13}`)
    },
    clickFavor () {
      this.addFavorite(this.bookDetail.isbn13)
    },
    getStoreInfo () {
      this.$http.get(`/book/collection/${this.bookDetail.isbn13}`).then(res => {
        this.storeInfo = res.data
      }).catch(err => console.log(err))
    },
    orderBook (id, isbn13, state) {
      if (state === '在架上') {
        this.$router.push(`/bookshelf/ordertime/${id}/${isbn13}`)
      } else if (state === '已经借出') {
        this.$http.post('/library/order/wait', {isbn13: isbn13, book_id: id}).then(res => {
          this.$vux.toast.show({
            text: '图书尚未归还，已加入预定栏'
          })
        }).catch(err => console.log(err))
      }
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
.part-body {
  font-size: 10px;
  max-height: 250px;
  overflow: hidden;
  padding: 10px 0;
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

.detail-box .store-box {
  margin: .15rem 0;
  padding: .08rem .15rem;
  background-color: #fff;
}
.store-table {
  width: 100%;
  text-align: center;
}

.table-item {
  font-size: 13px;
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
  padding: .05rem .15rem ;
  background-color: #fff;
}

.book-opt .i-btn-blank {
  margin: 0 5px;
  vertical-align: center;
}
.i-btn-icon {
  height: 12px;
  vertical-align: center;
  padding-right: 4px;
}
.part-title {
  color: #2bc2c3;
  display: flex;
  justify-content: space-between;
}
.more-icon {
  height: 14px;
  padding-right: 10px;
}
</style>
