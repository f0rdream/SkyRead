<template>
  <div class="app-wrapper">
    <x-header :right-options="{showMore: true}">个人信息</x-header>
    <section class="avatar-part">
      <img class="avatar" src="../../assets/logo.png">
      <p class="avatar-info">{{ username }}</p>
    </section>
    <group class="book-part">
      <clickable-list :books="books" labelText="想读的书"></clickable-list>
      <clickable-list :books="books" labelText="已借阅"></clickable-list>
      <clickable-list :books="books" labelText="已预订"></clickable-list>
      <clickable-list :books="books" labelText="想读的书"></clickable-list>
    </group>
    <group class="setting-part">
      <x-switch v-model="recommend" title="系统推荐"></x-switch>
      <x-switch v-model="orderRemind" title="预定提醒"></x-switch>
    </group>
    <group class="about-part">
      <cell title="关于我们"></cell>
      <cell title="意见反馈"></cell>
    </group>
    <bottom-bar activeTab="我的"></bottom-bar>
  </div>
</template>
<script>
import { XHeader, Group, Cell, XSwitch } from 'vux'
import ClickableList from '@/components/ClickableList'
import BottomBar from '@/components/BottomBar'

export default {
  components: {
    ClickableList,
    BottomBar,
    XHeader,
    Group,
    Cell,
    XSwitch
  },
  data () {
    return {
      username: '微信名字',
      recommend: true,
      orderRemind: true,
      books: ['1', '1', '1']
    }
  }
}
</script>
<style scoped>
.app-wrapper {
  height: 100%;
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
