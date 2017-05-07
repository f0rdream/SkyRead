<template>
  <div class="bar-wrapper vux-1px-t">
    <div class="bar-left" :class="activeTab === '首页' ? 'active' : ''">首页</div>
    <div class="bar-right" :class="activeTab === '我的' ? 'active' : ''">我的</div>
    <div class="bar-center">扫码借书</div>
  </div>
</template>
<script>
export default {
  props: {
    activeTab: String
  },
  data () {
    return {}
  },
  computed () {},
  mounted () {},
  methods: {}
}
</script>
<style>
.bar-wrapper {
  display: flex;
  position: fixed;
  bottom: 0;
  width: 100%;
  font-size: 12px;
  background-color: #f4f4f4;
}
.bar-wrapper .active {
  color: #2bc3c2;
}
.bar-wrapper .bar-left, .bar-wrapper .bar-right {
  width: 50%;
  text-align: center;
  padding: 15px 0;
}
.bar-wrapper .bar-left {
  padding-right: 34px;
}
.bar-wrapper .bar-right {
  padding-left: 34px;
}
.bar-center {
  background-color: #f4f4f4;
  height: 68px;
  line-height: 68px;
  width: 68px;
  position: absolute;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  border-radius: 50%;
  text-align: center;
  box-shadow: 0 0 5px #2bc0cb;
}
</style>
