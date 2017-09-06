<template lang="html">
<view-box class="app-wrapper">
  <div class="page-wrapper">
    <div class="header" slot="header">
      我的书单
    </div>
    <div class="tab-container">
      <button-tab v-model="selectedIndex" class="tab-self">
        <button-tab-item>我的</button-tab-item>
        <button-tab-item>收藏</button-tab-item>
      </button-tab>
    </div>
    <div class="item-container" v-for="item in myList">
      <div class="content-box">
        <div class="item-title">
          <span @click="$router.push(`/booklistdetail/${item.id}`)">{{item.title}}</span>
          <!-- <span @click="delNote(item.id)" class="rt-icon i-icon-container"><i class="i-icon-cross"></i></span> -->
        </div>
        <div class="item-content" @click="$router.push(`/booklistdetail/${item.id}`)">
          <span v-for="itemB in item.title_list" class="title-item">《{{itemB}}》 </span>
        </div>
      </div>
      <!-- <div class="opt-box">
        <div class="time">{{item.date}}</div>
        <div class="opt-icon">


          <span @click="modNote(item.id)">修改</span>
        </div>
      </div> -->
    </div>
    <div class="spinner-rb spinner" @click="addList">
      <i class="i-icon-plus"></i>
    </div>
  </div>
  <bottom-bar :activeTab="3" slot="bottom"></bottom-bar>
</view-box>
</template>

<script>
import { ButtonTab, ButtonTabItem, ViewBox } from 'vux'
import BottomBar from '@/components/BottomBar'
export default {
  components: {
    ViewBox,
    BottomBar,
    ButtonTab,
    ButtonTabItem
  },
  data () {
    return {
      selectedIndex: 0,
      myList: []
    }
  },
  watch: {
    selectedIndex (newValue) {
      switch (newValue) {
        case 0:
          this.getMine()
          break
        case 1:
          this.getFavor()
          break
      }
    }
  },
  mounted () {
    this.getMine()
  },
  methods: {
    getMine () {
      this.$http.get(`/accounts/book_list/`).then(res => {
        this.myList = res.data
      }).catch(err => console.log(err.response.data))
    },
    getFavor () {
      this.$http.get(`/accounts/book_list/star/`).then(res => {
        this.myList = res.data
      }).catch(err => console.log(err.response.data))
    },
    addList () {
      this.$router.push('/addbooklist')
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
  color: #818181;
  padding: .10rem .15rem;
  display: flex;
  justify-content: space-between;
}
/*.item-container {


  display: flex;
  flex-direction: column;
  justify-content: space-between;
}*/
.item-title {
  font-size: 15px;
  position: relative;
}
.rt-icon {
  position: absolute;
  top: 0;
  right: 0;
  display: inline-block;
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
  box-shadow: 1px 1px 1px 1px rgba(70, 70, 70, 0.1);
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

.content-box {
  overflow: hidden;
}
.tab-container {
  display: flex;
  padding: .10rem .15rem;
}
.tab-self {
  margin: auto;
  width: 50%;
}
.title-item {
  display: inline-block;
  word-wrap: normal;
  white-space: nowrap;
}
.i-icon-container {
  transform: scale(0.5);
}
.i-icon-cross {
  color: #000;
}
</style>
