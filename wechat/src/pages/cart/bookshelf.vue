<template lang="html">
  <view-box class="app">
    <!-- <x-header :right-options="{showMore: true}" slot="header">个人信息</x-header> -->
    <tab v-model="selectedIndex" bar-active-color="#2bc6b9" active-color="#2bc6b9">
      <tab-item @on-item-click="$router.replace('/bookshelf/scaned')">已扫码</tab-item>
      <tab-item @on-item-click="$router.replace('/bookshelf/ordered')">已预订</tab-item>
      <tab-item @on-item-click="$router.replace('/bookshelf/renting')">正在借阅</tab-item>
      <tab-item @on-item-click="$router.replace('/bookshelf/favorite')">收藏夹</tab-item>
      <tab-item @on-item-click="$router.replace('/bookshelf/readplan')">阅读计划</tab-item>
    </tab>
    <transition name="router-fade" mode="out-in">
      <router-view></router-view>
    </transition>
    <bottom-bar slot="bottom" :activeTab="2"></bottom-bar>
  </view-box>
</template>

<script>
import { ViewBox, Tab, TabItem } from 'vux'
import { mapActions } from 'vuex'
import BottomBar from '@/components/BottomBar'

export default {
  components: {
    ViewBox,
    Tab,
    TabItem,
    BottomBar
  },
  computed: {
    selectedIndex: {
      get () {
        return this.$store.state.currentTab
      },
      set (val) {
        this.setCurrentTab(val)
      }
    }
  },
  data () {
    return {
    }
  },
  watch: {
  },
  methods: {
    ...mapActions([
      'setCurrentTab'
    ])
  }
}
</script>

<style lang="css" scoped>
</style>
