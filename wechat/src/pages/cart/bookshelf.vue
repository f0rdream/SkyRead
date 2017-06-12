<template lang="html">
  <view-box class="app">
    <!-- <x-header :right-options="{showMore: true}" slot="header">个人信息</x-header> -->
    <tab>
      <tab-item @on-item-click="router.push('scaned')">扫码的书</tab-item>
      <tab-item @on-item-click="router.push('lending')">正在借阅</tab-item>
    </tab>
    <transition name="router-fade" mode="out-in">
      <router-view></router-view>
    </transition>
    <bottom-bar slot="bottom"></bottom-bar>
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
  methods: {}
}
</script>

<style lang="css">
</style>
