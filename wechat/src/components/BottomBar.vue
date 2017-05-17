<template>
  <div class="bar-wrapper vux-1px-t">
    <div class="" :class="activeTab === 'currentTabs[0]' ? 'active' : ''">{{currentTabs[0]}}</div>
    <div class="bar-left" :class="activeTab === 'currentTabs[1]' ? 'active' : ''">{{currentTabs[1]}}</div>
    <div class="bar-right" :class="activeTab === 'currentTabs[2]' ? 'active' : ''">{{currentTabs[2]}}</div>
    <div class="" :class="activeTab === 'currentTabs[3]' ? 'active' : ''">{{currentTabs[3]}}</div>
    <div class="bar-center">扫码借书</div>
  </div>
</template>
<script>
export default {
  props: {
    activeTab: String,
    tabs: Array
  },
  data () {
    return {}
  },
  computed: {
    currentTabs () {
      let defaultTabs = ['首页', '搜索', '书架', '我的']
      return this.tabs || defaultTabs
    }
  },
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
  flex-flow: row nowrap;
}
.bar-wrapper .active {
  color: #2bc3c2;
}
.bar-wrapper>div:not(.bar-center) {
  text-align: center;
  padding-top: 15px;
  padding-bottom: 15px;
  width: 25%;
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
