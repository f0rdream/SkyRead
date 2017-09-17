<template lang="html">
  <div class="page-wrapper">
    <tab v-model="selectedIndex" bar-active-color="#2bc6b9" active-color="#2bc6b9">
      <tab-item v-for="item in tabItems" :key="item.src">{{item.label}}</tab-item>
    </tab>
    <div class="item-container" v-for="item in items" :key="item.id">
      <div class="upper">
        <img :src="item.headimgurl" class="head-img">
        <div class="name-container">
          <span class="name-text">{{ item.nick_name }}</span>
          <span class="name-after">分享{{ item.type === 'note' ? '笔记' : '书单'}}</span>
        </div>
      </div>
      <div class="lower">
        <div class="left">
          <img :src="getImg(item.img_id)" class="list-img" @click="itemClick(item.id, item.type)">
        </div>
        <div class="right">
          <div class="item-title">{{ item.title }}</div>
          <div class="item-comment i-ellipsis-4">{{ item.comment }}</div>
        </div>
      </div>
    </div>
    <infinite-loading :on-infinite="onInfinite" ref="infiniteLoading"></infinite-loading>
  </div>
</template>

<script>
import { Tab, TabItem } from 'vux'
import InfiniteLoading from 'vue-infinite-loading'

export default {
  components: {
    Tab,
    TabItem,
    InfiniteLoading
  },
  data () {
    return {
      tabItems: [
        { label: '最新' },
        { label: '最热' }
      ],
      pageNum: 1,
      items: [],
      orderType: ['star', 'time'],
      selectedIndex: 0
    }
  },
  watch: {
    selectedIndex (newValue) {
      switch (newValue) {
        case 0:
          this.pageNum = 1
          this.items = []
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:reset')
          break
        case 1:
          this.pageNum = 1
          this.items = []
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:reset')
          break
      }
    }
  },
  methods: {
    onInfinite () {
      this.$http.get(`/accounts/cycle/${this.pageNum}/?order=${this.orderType[this.selectedIndex]}`).then((res) => {
        if (res.data.length !== 0) {
          this.items = this.items.concat(res.data)
          this.pageNum += 1
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:loaded')
        } else {
          this.$refs.infiniteLoading.$emit('$InfiniteLoading:complete')
        }
      }).catch((err) => {
        console.error(err)
      })
    },
    getImg (imgId) {
      return imgId && imgId !== '--' ? `https://img3.doubanio.com/lpic/${imgId}` : '/static/others/nocover.png'
    },
    itemClick (id, type) {
      console.log(id, type)
      if (type === 'note') {
        this.$router.push(`/notedetail/${id}`)
      } else if (type === 'book_list') {
        this.$router.push(`/booklistdetail/${id}`)
      }
    }

  }
}
</script>

<style lang="css" scoped>
.item-container {
  margin-top: .15rem;
  background: #fff;
  padding: .10rem .15rem;
}
.head-img, .name-container {
  vertical-align: middle;
}
.head-img {
  height: 35px;
  width: 35px;
  border-radius: 50%;
}
.name-container {
  display: inline-block;
  margin-left: .10rem;
}
.name-text {
  color: #636363;
  font-size: 16px;
}
.name-after {
  margin-left: .10rem;
  font-size: 12px;
  color: #8d8d8d;
}

.lower {
  margin-top: .10rem;
  background-color: #efefef;
  display: flex;
  box-shadow: 0 0 1px 1px rgba(70, 70, 70, 0.1);
}
.left {
  flex: 0 0 25%;
  line-height: 1;
}
.right {
  padding-left: .15rem;
  flex: 1 1 auto;
  overflow: hidden;
}
.list-img {
  width: 100%;
}

.item-title {
  color: #8d8d8d;
  font-size: 16px;
}
.item-comment {
  margin-top: .08rem;
  white-space: normal;
  color: #8d8d8d;
  word-wrap: break-word;
  font-size: 12px;
}
</style>
