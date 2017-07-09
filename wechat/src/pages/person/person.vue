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
    <group class="about-part">
      <cell title="关于我们"></cell>
    </group>
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
      historyList: []
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
      }).catch(err => console.log(err))
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
</style>
