<template>
  <div class="bar-wrapper vux-1px-t">
    <div :class="activeTab === currentTabs[0] ? 'active' : ''" @click="$router.push(currentTabs[0].url)">{{currentTabs[0].name}}</div>
    <div class="bar-left" :class="activeTab === currentTabs[1] ? 'active' : ''" @click="$router.push(currentTabs[1].url)">{{currentTabs[1].name}}</div>
    <div class="bar-right" :class="activeTab === currentTabs[2] ? 'active' : ''" @click="$router.push(currentTabs[2].url)">{{currentTabs[2].name}}</div>
    <div :class="activeTab === currentTabs[3] ? 'active' : ''" @click="$router.push(currentTabs[3].url)">{{currentTabs[3].name}}</div>
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
      let defaultTabs = [
        {
          name: '首页',
          url: '/home/indexpage'
        },
        {
          name: '搜索',
          url: '/search'
        },
        {
          name: '书架',
          url: '/bookshelf'
        },
        {
          name: '个人',
          url: '/person'
        }
      ]
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
