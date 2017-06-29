<template>
  <view-box class="app">
    <!-- <x-header :right-options="{showMore: true}" slot="header">个人信息</x-header> -->
    <transition name="router-fade" mode="out-in">
      <router-view></router-view>
    </transition>
    <bottom-bar slot="bottom" :activeTab="0"></bottom-bar>
  </view-box>
</template>

<script>
import Search from '@/components/SearchBar'
import BottomBar from '@/components/BottomBar'
import { XHeader, ViewBox } from 'vux'

export default {
  components: {
    Search,
    BottomBar,
    XHeader,
    ViewBox
  },
  data () {
    return {}
  }
}
</script>

<style lang="css" scoped>
</style>
