
<template lang="html">
  <section class="main-part">
    <swiper :list="imgList" v-model="imgIndex" :auto="true" :loop="true"></swiper>
    <div class="category">
      <div class="cate-item" v-for="(value, key) in bookTypes" v-if="key < 8 || isMore">
        <a @click="getToCate(key)">
          <img :src="value.img" class="cate-img">
          <p class="cate-item-string">{{ value.type }}</p>
        </a>
      </div>
      <div class="cate-item cate-item-rear" @click="isMore = !isMore">
        <img src="/static/class/more.png" class="cate-img">
        <p class="cate-item-string">
          {{ isMore ? '收起分类' : '更多分类'}}
        </p>
      </div>
    </div>
    <recommend-card :bookItems="recommendBooks"></recommend-card>
    <!-- <related-person></related-person> -->
  </section>
</template>

<script>
import { Swiper } from 'vux'
import RecommendCard from '@/components/RecommendCard'
import RelatedPerson from '@/components/RelatedPerson'
import { bookTypes } from '@/config/data'

export default {
  components: {
    Swiper,
    RecommendCard,
    RelatedPerson
  },
  data () {
    return {
      isMore: false,
      bookTypes: bookTypes,
      recommendBooks: [],
      imgList: [],
      imgIndex: 0
    }
  },
  mounted () {
    this.getRecommend()
    this.getSwiper()
  },
  methods: {
    getRecommend () {
      this.$http.get('/list/recommend/').then(res => {
        this.recommendBooks = res.data
      }).catch(err => console.warn(err))
    },
    getSwiper () {
      this.$http.get('/picture/').then(res => {
        for (let item of res.data) {
          this.imgList.push({url: `/home/bookdetail/${item.isbn13}`, img: item.picture, title: item.title})
        }
      }).catch(err => console.log(err))
    },
    getToCate (key) {
      if (key < 15) {
        this.$router.push(`/home/category/${key}`)
      }
    }
  }
}
</script>

<style lang="css" scoped>
.category {
  display: flex;
  flex-flow: row wrap;
  background-color: #fff;
  padding: .15rem .15rem;
  justify-content: space-between;
}
.cate-item {
  text-align: center;
  color: #5f5f5f;
  font-size: 12px;
  flex: 0 1 21%;
}
.cate-item-rear {
  align-self: flex-end;
}
.cate-img {
  width: 50%;
}
.cate-item-string {
  color: #5f5f5f;
}
</style>
