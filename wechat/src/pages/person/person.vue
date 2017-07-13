<template>
  <view-box class="app-wrapper">
    <!-- <x-header :right-options="{showMore: true}">个人信息</x-header> -->
    <section class="avatar-part">
      <img class="avatar" :src="userInfo.headimgurl">
      <p class="avatar-info">{{ userInfo.nickname }}</p>
    </section>
    <group class="book-part">
      <clickable-list :books="historyList" labelText="借阅历史"></clickable-list>
    </group>
    <group class="setting-part">
      <x-switch v-model="backRemind" title="还书提醒"></x-switch>
    </group>
    <group class="about-part">
      <cell title="手机信息" :is-link="true" :link="'/person/phone'">
        <span>{{ userInfo.phone_number }}</span>
      </cell>
      <!-- <cell title="绑定信息"></cell> -->
    </group>
    <div class="setting-part">
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
      </div>
    </div>
    <bottom-bar :activeTab="3" slot="bottom"></bottom-bar>
  </view-box>
</template>
<script>
import { XHeader, Group, Cell, XSwitch, ViewBox } from 'vux'
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
    ViewBox
  },
  data () {
    return {
      backRemind: true,
      historyList: [],
      isSettingSpread: true
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
  height: 1.5rem;
}
.avatar {
  margin-top: .15rem;
  height: 1rem;
  width: 1rem;
  border-radius: 50% 50%;
}
.cell-item {
  display: flex;
  justify-content: space-between;
  margin-top: .15rem;
  padding: 8px 15px;
  background-color: #fff;
}
.cell-item .label-btn {
  color: #858585;
  font-size: 12px;
  line-height: 27px;
}
.cell-addon {
  display: flex;
  flex-direction: row;
}
.app-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  max-width: 25%;
  margin: 10px 10px;
}
.app-img {
  width: 50%;
}
.app-title {
  font-size: 14px;
  color: #333;
}
</style>
