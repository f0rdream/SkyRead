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
            <div class="right-container">
              <p class="body-title ellipsis">{{ bookDetail.title }}</p>
              <p class="body-info info-author">作者：<router-link v-for="item in bookDetail.author" class="info-link" :to="`/home/list/author/${item}`" :key="bookDetail.author">{{item}}, </router-link></p>
              <p class="body-info">出版社：{{ bookDetail.publisher }}</p>
              <p class="body-info">出版时间：{{ bookDetail.pubdate }}</p>
              <p class="body-info">豆瓣评分：{{ bookDetail.average }}</p>
            </div>
          </div>
        </div>
        <div class="book-opt">
          <div class="left"></div>
          <div class="right">
            <tab bar-active-color="#2bc6b9" active-color="#2bc6b9" v-model="selectedIndex">
              <tab-item>简介</tab-item>
              <tab-item>书评</tab-item>
              <tab-item>导读</tab-item>
            </tab>
            <!-- <a class="i-btn-blank" @click="clickFavor"><img src="/static/others/collect.png" class="i-btn-icon">收藏</a>
            <a class="i-btn-blank" @click="comment"><img src="/static/others/comment.png" class="i-btn-icon">评论</a> -->
          </div>
        </div>
      </div>
      <div class="detail-part">
        <div class="book-description part-main" v-if="selectedIndex === 0">
          <div class="description-context-box">
            <div class="description-context" :class="{ 'i-ellipsis': !isContentUnfold }">{{ bookDetail.summary }}</div>
            <div class="icon-container" @click="isContentUnfold = !isContentUnfold">
              <img class="more-icon" :src="!isContentUnfold ? '/static/others/unfold.png' : '/static/others/fold.png'" ></img>
            </div>
            <div class="des-tags">
              <router-link v-for="item in bookDetail.tags" :to="`/home/list/tag/${item}`" :key="bookDetail.tags" class="tag-link">{{ item }}</router-link>
            </div>
          </div>
          <div class="opt-part">
            <div class="opt-item" @click="clickFavor">
              <img src="/static/others/collect.png" class="opt-icon">
              <div class="opt-text">收藏</div>
            </div>
            <div class="opt-item" @click="comment">
              <img src="/static/others/comment.png" class="opt-icon">
              <div class="opt-text">评论</div>
            </div>
            <div class="opt-item" @click="price">
              <img src="/static/others/comment.png" class="opt-icon">
              <div class="opt-text">购书比价</div>
            </div>
          </div>
          <div class="store-box">
            <p class="part-title" @click="isTableUnfold = !isTableUnfold">
              <span>馆藏信息</span>
              <img class="more-icon" :src="!isTableUnfold ? '/static/others/unfold.png' : '/static/others/fold.png'"></img>
            </p>
            <table class="store-table" v-show="isTableUnfold">
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
          <div class="related">
            <p class="part-title">
              <span>相关书籍</span>
            </p>
            <div class="related-container">
              <div v-for="item in related" class="related-item">
                <img :src="getImg(item.img_id)" class="item-img" @click="relatedClick(item.isbn13)">
                <p class="item-title">{{ item.title }}</p>
              </div>
            </div>
          </div>
        </div>
        <div class="book-review part-main" v-if="selectedIndex === 1">
          <div class="review-detail" v-for="item in reviewList">
            <div class="review-title">{{item.title}}</div>
            <div class="review-author">{{item.author}}</div>
            <div class="review-content-container">
              <div class="review-content" :class="{ 'i-ellipsis': !isReviewUnfold }">{{ item.content }}</div>
              <div class="icon-container" @click="isReviewUnfold = !isReviewUnfold">
                <img class="more-icon" :src="!isReviewUnfold ? '/static/others/unfold.png' : '/static/others/fold.png'" ></img>
              </div>
            </div>
          </div>
        </div>
        <div class="book-trail part-main" v-if="selectedIndex === 2">
          <pre v-html="bookDetail.catalog" class="index-body"></pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { XImg, Tab, TabItem } from 'vux'
import { mapActions } from 'vuex'
export default {
  components: {
    XImg,
    Tab,
    TabItem
  },
  data () {
    return {
      isbn13: this.$route.params.isbn13,
      bookDetail: {},
      isContentUnfold: false,
      isTableUnfold: false,
      isReviewUnfold: false,
      storeInfo: {},
      selectedIndex: 0,
      reviewList: [1, 1],
      related: []
    }
  },
  mounted () {
    this.getBook()
    this.getReview()
    this.getRelated()
  },
  watch: {
    '$route' (to, from) {
      this.getBook()
      this.getReview()
      this.getRelated()
    }
  },
  methods: {
    ...mapActions({
      addFavorite: 'addFavorite'
    }),
    getBook () {
      this.isbn13 = this.$route.params.isbn13
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
        console.log(err.response.data)
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
      }).catch(err => console.log(err.response.data))
    },
    orderBook (id, isbn13, state) {
      if (state === '在架上') {
        this.$router.push(`/bookshelf/ordertime/${id}/${isbn13}`)
      } else if (state === '已经借出') {
        this.$http.post('/library/order/wait', {isbn13: isbn13, book_id: id}).then(res => {
          this.$vux.toast.show({
            text: '图书尚未归还，已加入预定栏'
          })
        }).catch(err => console.log(err.response.data))
      }
    },
    getReview () {
      this.$http.get(`/douban/reviews/${this.isbn13}`).then(res => {
        this.reviewList = res.data
      }).catch(err => {
        console.log(err.response.data)
      })
    },
    getRelated () {
      this.$http.get(`/book/refer/${this.isbn13}`).then(res => {
        this.related = res.data
      }).catch(err => {
        console.log(err.response.data)
      })
    },
    getImg (imgId) {
      return `https://img3.doubanio.com/lpic/${imgId}`
    },
    relatedClick (isbn13) {
      this.$router.push(`/home/bookdetail/${isbn13}`)
    },
    price () {
      this.$router.push(`/home/price/${this.isbn13}`)
    }
  }
}
</script>

<style lang="css" scoped>
.detail-box>div {
  /*Background color*/
  background-color: #f7f6f6;
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
  flex: 1 1 auto;
  padding: 0 0.10rem;
  overflow: hidden;
}
.right-container {
  position: relative;
  top: 25px;
}
.book-opt .right {
  flex: 1 1 auto;
  padding: 0 0;
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
  background-color: #f1f2f7;
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

.description-context {
  padding: .08rem;
  font-size: 14px;
  overflow: hidden;
}
.tag-link {
  display: inline-block;
  background-color: #fff;
  color: #707070;
  margin: .05rem .08rem;
  padding: 5px 10px;
  text-decoration: none;
  border-radius: 15px;
  font-size: 12px;
}
.description-context-box .icon-container {
  text-align: right;
}
.part-main>div {
  background-color: #f1f2f7;
  padding: .08rem .10rem;
  margin-bottom: .10rem;
}
.part-main {
  margin: 0 0 .10rem 0;
  background-color: #f7f6f6;
  color: #5c5c5c;
}
.body-info.info-author {
  overflow: visible;
  white-space: normal;
}

.opt-part {
  display: flex;
  flex-direction: row;
}
.opt-icon {
  height: 25px;
  width: 25px;
}
.opt-item {
  padding: .08rem;
  display: flex;
  flex-direction: column;
  text-align: center;
  align-items: center;
  font-size: 13px;
  flex: 0 1 20%;
}

.index-body {
  padding: .15rem .25rem;
  font-size: 13px;
}

.related-container {
  white-space: nowrap;
  overflow: scroll;
}
.related-item {
  display: inline-block;
  width: 19%;
  margin: .10rem;
}
.related-item .item-img {
  width: 100%;
}
.related-item .item-title {
  font-size: 12px;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

/* review title*/
.review-title {
  font-size: 15px;
}
.review-author {
  font-size: 13px;
}
.review-content {
  font-size: 13px;
}
.review-content-container .icon-container {
  text-align: right;
}

</style>
