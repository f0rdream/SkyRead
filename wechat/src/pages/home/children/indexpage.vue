
<template lang="html">
  <section class="main-part">
    <swiper :list="imgList" v-model="imgIndex"></swiper>
    <div class="category">
      <div class="cate-item" v-for="(value, key) in bookTypes" v-if="key < 8 || isMore">
        <router-link :to="`/home/category/${ key }`">
          <img :src="value.img" class="cate-img">
          <p class="cate-item-string">{{ value.type }}</p>
        </router-link>
      </div>
      <div class="cate-item" @click="toggleMore">
        <img src="/static/class/more.png" class="cate-img">
        <p class="cate-item-string">
          {{ isMore ? '收起分类' : '更多分类'}}
        </p>
      </div>
    </div>
    <recommend-card :bookItems="recommendBooks" ></recommend-card>
    <related-person></related-person>
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
      imgList: [
        {
          url: 'javascript:',
          img: 'https://static.vux.li/demo/1.jpg',
          title: '送你一朵fua'
        },
        {
          url: 'javascript:',
          img: 'https://static.vux.li/demo/2.jpg',
          title: '送你一辆车'
        },
        {
          url: 'javascript:',
          img: 'https://static.vux.li/demo/3.jpg',
          title: '送你一次旅行'
        }
      ],
      imgIndex: 0
    }
  },
  mounted () {
    this.getRecommend()
  },
  methods: {
    getRecommend () {
      this.$http.get('/list/recommend/').then(res => {
        this.recommendBooks = res.data
      }).catch(err => console.warn(err))
    },
    toggleMore () {
      this.isMore = !this.isMore
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
.cate-img {
  width: 50%;
}
.cate-item-string {
  color: #5f5f5f;
}
</style>
