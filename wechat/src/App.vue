<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import './style/common.css'
export default {
  name: 'app'
}
</script>

<style lang="less">
@import '~vux/src/styles/reset.less';
@import '~vux/src/styles/1px.less';

#app {
  height: 100%;
}
</style>
