<template lang="html">
  <view-box class="app">
    <!-- <x-header :right-options="{showMore: true}" slot="header">个人信息</x-header> -->
    <div class="cart-banner">

    </div>
    <tab v-model="selectedIndex" bar-active-color="#2bc6b9" active-color="#2bc6b9">
      <tab-item v-for="item in tabItems" @on-item-click="$router.replace(item.src)" :key="item.src">{{item.label}}</tab-item>
    </tab>
    <transition name="router-fade" mode="out-in">
      <router-view></router-view>
    </transition>
    <bottom-bar slot="bottom" :activeTab="2"></bottom-bar>
  </view-box>
</template>

<script>
import { tabItems } from '@/config/data'
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
    // TODO 可维护的index链接及列表
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
      tabItems: tabItems
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
