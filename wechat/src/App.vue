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

body {
  background-color: #fbfbfb;
}
html {
  font-size: 100px;
}
body {
  font-size: 16px;
}
</style>
