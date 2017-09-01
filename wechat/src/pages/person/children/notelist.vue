<template lang="html">
<view-box class="app-wrapper">
  <div class="page-wrapper">
    <div class="header" slot="header">
      我的笔记
    </div>
    <div class="item-container" v-for="item in noteList">
      <div class="left">
        <div class="content-box">
          <div class="item-title">{{item.title}}</div>
          <div class="item-content i-ellipsis">{{item.comment}}</div>
        </div>
        <div class="opt-box">
          <div class="time">{{item.date}}</div>
          <div class="opt-icon">
            <!--TODO To add icons  -->
            <span @click="delNote(item.id)">删除</span>
            <span @click="modNote(item.id)">修改</span>
          </div>
        </div>
      </div>
      <div class="right">
        <img :src="getImg(item.book_img_url)" class="book-img">
      </div>
    </div>
    <div class="spinner-rb spinner" @click="addNote">
      <i class="i-icon-plus"></i>
    </div>
  </div>
  <bottom-bar :activeTab="3" slot="bottom"></bottom-bar>
</view-box>
</template>

<script>
import BottomBar from '@/components/BottomBar'
import { ViewBox } from 'vux'
export default {
  components: {
    ViewBox,
    BottomBar
  },
  data () {
    return {
      noteList: []
    }
  },
  mounted () {
    this.getNotes()
  },
  methods: {
    getNotes () {
      this.$http.get(`/book/note/`).then(res => {
        this.noteList = res.data
      }).catch(err => console.log(err))
    },
    getImg (imgId) {
      return `https://img3.doubanio.com/lpic/${imgId}`
    },
    delNote (id) {
      this.$http.delete(`/book/note/${id}`).then(res => {
        this.getNotes()
      }).catch(err => console.log(err))
    },
    modNote (id) {
      this.$router.push('/modnote')
    },
    addNote () {
      this.$router.push('/addnote')
    }
  }
}
</script>

<style lang="css" scoped>
.header {
  text-align: center;
  padding: .08rem .15rem;
  background-color: #2aebc8;
  color: #fff;
}
.item-container {
  margin-top: .13rem;
  background-color: #fff;
  box-shadow: 0px 1px 2px 1px rgba(0, 0, 0, 0.1);
  display: flex;
  justify-content: space-between;
}
.right {
  flex: 0 0 28%;
  overflow: hidden;
}
.right>img {
  display: block;
  width: 100%;
}
.left {
  flex: 1 1 auto;
  padding: .10rem .15rem;
  color: #818181;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}
.item-title {
  font-size: 15px;
}
.item-content {
  padding-top: .08rem;
  font-size: 12px;
}
.opt-box {
  font-size: 12px;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
}
.spinner {
  position: fixed;
  width: 40px;
  height: 40px;
  background: #25d398;
  border-radius: 50%;
  display: flex;
}
.spinner:active {
  background: #64d3ad;
}
.spinner>i {
  margin: auto;
}
.spinner-rb {
  bottom: 70px;
  right: 20px;
}
</style>
