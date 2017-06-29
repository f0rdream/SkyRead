<template lang="html">
  <div class="book-card">
    <div class="book-nav">
      <span>猜你喜欢</span>
      <span>换一本</span>
    </div>
    <div class="book-body">
      <div class="left">
        <img :src="'https://img3.doubanio.com/lpic/' + recommendDetail.img_id" class="book-img">
        <p class="body-title ellipsis">{{ recommendDetail.title }}</p>
        <div class="opt-box">
          <!--  TODO  添加收藏的mutation -->
          <router-link to="">推荐</router-link>
          <router-link to="">收藏</router-link>
        </div>
      </div>
      <div class="right">
        <p class="body-info">作者：{{ recommendDetail.author }}</p>
        <p class="body-info">作者简介：{{ recommendDetail.author_intro }}</p>
        <p class="body-info">出版社：{{ recommendDetail.publisher }}</p>
        <p class="body-info">出版时间：{{ recommendDetail.pubdate }}</p>
        <p class="body-info">价格：{{ recommendDetail.price }}</p>
        <p class="body-info">ISBN：{{ recommendDetail.isbn13 }}</p>
        <p class="body-info">页数：{{ recommendDetail.pages }}页</p>
        <p class="body-info">标签： <router-link v-for="item in recommendDetail.tags" to="" :key="recommendDetail.tags">{{ item }} </router-link></p>
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
            <p class="times-score">{{ recommendDetail.average }}</p>
            <p>豆瓣评分</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    recommendDetail: Object
  }
}
</script>

<style lang="css" scoped>
.book-card {
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
</style>
