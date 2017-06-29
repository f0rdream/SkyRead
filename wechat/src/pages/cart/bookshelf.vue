<template lang="html">
  <view-box class="app">
    <!-- <x-header :right-options="{showMore: true}" slot="header">个人信息</x-header> -->
    <tab v-model="selectedIndex">
      <tab-item @on-item-click="$router.replace('/bookshelf/scaned')">已扫码</tab-item>
      <tab-item @on-item-click="$router.replace('/bookshelf/ordered')">已预订</tab-item>
      <tab-item @on-item-click="$router.replace('/bookshelf/lending')">正在借阅</tab-item>
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
import BottomBar from '@/components/BottomBar'

export default {
  components: {
    ViewBox,
    Tab,
    TabItem,
    BottomBar
  },
  data () {
    return {
      selectedIndex: 0
    }
  },
  watch: {
  },
  methods: {
  }
}
</script>

<style lang="css" scoped>
</style>
