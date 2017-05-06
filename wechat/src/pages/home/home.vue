<template>
  <div>
    <x-header :right-options="{showMore: true}">个人信息</x-header>
    <search placeholder="搜索书籍"></search>
    <transition name="router-fade" mode="out-in">
      <router-view></router-view>
    </transition>
    <bottom-bar></bottom-bar>
  </div>
</template>

<script>
import Search from '@/components/SearchBar'
import BottomBar from '@/components/BottomBar'
import { XHeader } from 'vux'

export default {
  components: {
    Search,
    BottomBar,
    XHeader
  },
  data () {
    return {}
  }
}
</script>

<style lang="css">
</style>
