<template lang="html">
  <baidu-map ak="QwNC9WunLAY2cGx4DCxzwLuXypwOWzLv" @ready="getMap">
    <bm-view class="map"></bm-view>
    <bm-transit :start="start" :end="end" :auto-viewport="true" :location="location"></bm-transit>
  </baidu-map>
</template>

<script>
import { BaiduMap, BmTransit, BmView } from 'vue-baidu-map'
export default {
  components: {
    BaiduMap,
    BmTransit,
    BmView
  },
  data () {
    return {
      // start: {lng: 114, lat: 30},
      // end: {lng: 114.369348, lat: 30.541621},
      // location: '北京'
      start: {lng: 0, lat: 0},
      end: {lng: 0, lat: 0},
      location: '北京'
    }
  },
  methods: {
    getMap ({BMap, map}) {
      // this.$wechat.getLocation({
      //   type: 'wgs84', // 默认为wgs84的gps坐标，如果要返回直接给openLocation用的火星坐标，可传入'gcj02'
      //   success: function (res) {
      //       this.start.latitude = res.latitude // 纬度，浮点数，范围为90 ~ -90
      //       this.start.longitude = res.longitude // 经度，浮点数，范围为180 ~ -180
      //   }
      // })
      console.log(BMap, map)
      this.start = "{lng: 114.365415, lat: 30.535169}"
      this.end = "{lng: '114.365415', lat: '30.535169'}"
      this.location = '武汉'
    }
  }
}
</script>

<style lang="css" scoped>
.map {
  width: 100%;
  height: 300px;
}
</style>
