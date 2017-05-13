<template lang="html">
  <section class="main-part">
    <swiper :list="imgList" v-model="imgIndex"></swiper>
    <div class="category">
      <div class="cate-item">马列主义</div>
      <div class="cate-item">哲学宗教</div>
      <div class="cate-item">自然科学</div>
      <div class="cate-item">数理科学</div>
      <div class="cate-item">社会科学</div>
      <div class="cate-item">政治法律</div>
      <div class="cate-item">工业技术</div>
      <div class="cate-item">更多分类</div>
       <!--TODO
       Add the more cate page
       -->
    </div>
    <item-viewer :items="books"></item-viewer>
  </section>
</template>

<script>
import { Swiper } from 'vux'
import ItemViewer from '@/components/ItemViewer'

export default {
  components: {
    Swiper,
    ItemViewer
  },
  data () {
    return {
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
      imgIndex: 0,
      books: [
        {
          img: '',
          title: '资治通鉴',
          isbn: '123456'
        },
        {
          img: '',
          title: '资治通鉴',
          isbn: '123456'
        },
        {
          img: '',
          title: '资治通鉴',
          isbn: '123456'
        },
        {
          img: '',
          title: '资治通鉴',
          isbn: '123456'
        },
        {
          img: '',
          title: '资治通鉴',
          isbn: '123456'
        },
        {
          img: '',
          title: '资治通鉴',
          isbn: '123456'
        }
      ]
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
</style>
