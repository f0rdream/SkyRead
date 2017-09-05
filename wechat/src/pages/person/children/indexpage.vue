<template>
  <view-box class="app-wrapper">
    <!-- <x-header :right-options="{showMore: true}">个人信息</x-header> -->
    <section class="avatar-part">
      <img class="avatar" :src="userInfo.headimgurl">
      <p class="avatar-info">{{ userInfo.nickname }}</p>
    </section>
    <div class="content-part">
      <tab v-model="selectedIndex" active-color="#3ed6bf" bar-active-color="#3ed6bf">
        <tab-item v-for="item in tabItems" :key="item.src">{{ item }}</tab-item>
      </tab>
      <div class="tab-content">
        <div class="history-box" v-if="selectedIndex === 0">
          <div class="history-item" v-for="item in historyList">
            <div class="left">
              <img :src="getImg(item.image)" class="list-img">
            </div>
            <div class="right">
              <div class="item-title">{{ item.title }}</div>
              <div class="item-info">借阅时间 {{ item.borrow_time }}</div>
              <div class="item-info">还书时间 {{ item.return_time }}</div>
            </div>
          </div>
        </div>
        <div class="find-box" v-if="selectedIndex === 1">
          <grid :rows="4">
            <grid-item :label="item.label" v-for="item in findItems" :link="item.src">
              <img slot="icon" :src="item.img">
            </grid-item>
          </grid>
        </div>
        <div class="history-box" v-if="selectedIndex === 2">
          <group class="about-part">
            <x-switch v-model="backRemind" title="还书提醒"></x-switch>
            <cell title="手机信息" :is-link="true" :link="'/person/phone'">
              <span>{{ userInfo.phone_number }}</span>
            </cell>
            <!-- <cell title="绑定信息"></cell> -->
          </group>
        </div>
      </div>
    </div>

    <!-- <group class="about-part">
      <clickable-list :books="historyList" labelText="借阅历史"></clickable-list>
      <cell title="手机信息" :is-link="true" :link="'/person/phone'">
        <span>{{ userInfo.phone_number }}</span>
      </cell>
    </group> -->
    <!-- <div class="setting-part">
      <div class="cell-item" :class="isSettingSpread ? 'vux-1px-t' : 'vux-1px-tb'">
        <span class="label-text">发现</span>
        <span class="label-btn" @click="isSettingSpread = !isSettingSpread">{{ isSettingSpread ? '收起' : '展开'}}</span>
      </div>
      <div class="cell-addon" v-show="isSettingSpread">
        <div class="app-item" @click="$router.push('/person/related')">
          <img class="app-img" src="/static/others/similarity.png">
          <p class="app-title">相似用户</p>
        </div>
        <div class="app-item" @click="$router.push('/person/nearby')">
          <img class="app-img" src="/static/others/nearby.png">
          <p class="app-title">附近的书</p>
        </div>
        <div class="app-item" @click="$router.push('/person/map')">
          <img class="app-img" src="/static/others/nearby.png">
          <p class="app-title">导航</p>
        </div>
        <div class="app-item" @click="$router.push('/feedback')">
          <img class="app-img" src="/static/others/nearby.png">
          <p class="app-title">反馈</p>
        </div>
        <div class="app-item" @click="$router.push('/modnote')">
          <img class="app-img" src="/static/others/nearby.png">
          <p class="app-title">反馈</p>
        </div>
      </div>
    </div> -->
    <bottom-bar :activeTab="3" slot="bottom"></bottom-bar>
  </view-box>
</template>
<script>
import { findItems } from '@/config/data'
import { XHeader, Group, Cell, XSwitch, ViewBox, Tab, TabItem, Grid, GridItem } from 'vux'
import { mapState } from 'vuex'
import ClickableList from '@/components/ClickableList'
import BottomBar from '@/components/BottomBar'

export default {
  components: {
    ClickableList,
    BottomBar,
    XHeader,
    Group,
    Cell,
    XSwitch,
    ViewBox,
    Tab,
    TabItem,
    Grid,
    GridItem
  },
  data () {
    return {
      selectedIndex: 0,
      tabItems: ['借阅历史', '发现', '设置'],
      backRemind: true,
      historyList: [],
      isSettingSpread: true,
      findItems
    }
  },
  computed: {
    ...mapState({
      userInfo: 'accountsInfo'
    })
  },
  mounted () {
    this.getHistory()
  },
  methods: {
    getHistory () {
      this.$http.get('/library/readed/').then(res => {
        this.historyList = res.data
      }).catch(err => console.log(err.response.data))
    },
    getImg (imgId) {
      return imgId ? `https://img3.doubanio.com/lpic/${imgId}` : null
    }
  }
}
</script>
<style scoped>
.app-wrapper {
  background-color: #fbfbfb;
}
.avatar-part {
  text-align: center;
  min-height: 1.8rem;
  background-image: url("/static/banner/personBG.png")
}
.avatar {
  margin-top: .30rem;
  height: .8rem;
  width: .8rem;
  border-radius: 50% 50%;
}
.avatar-info {
  color: #fff;
}



.history-item {
  margin: .10rem .15rem;
  background-color: #fff;
  color: #767676;
  display: flex;
  box-shadow: 1px 1px 1px 1px rgba(70, 70, 70, 0.1);
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
.item-info {
  font-size: 14px;
}
.item-comment {
  margin-top: .08rem;
  white-space: normal;
  color: #8d8d8d;
  word-wrap: break-word;
  font-size: 12px;
}
</style>
