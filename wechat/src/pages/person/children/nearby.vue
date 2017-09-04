<template lang="html">
  <div class="title-container">
    <div class="title">
      <p class="title-string">你附近的书</p>
    </div>
    <list-item v-for="item in itemList"  :itemInfo="item" :key="item.isbn13"></list-item>
  </div>
</template>

<script>
import ListItem from '@/components/ListItem'
export default {
  components: {
    ListItem
  },
  data () {
    return {
      itemList: []
    }
  },
  mounted () {
    this.sendLoc()
    this.getList()
  },
  methods: {
    sendLoc () {
      let xPoint, yPoint
      this.$wechat.getLocation({
        type: 'wgs84', // 默认为wgs84的gps坐标，如果要返回直接给openLocation用的火星坐标，可传入'gcj02'
        success: function (res) {
          xPoint = res.latitude // 纬度，浮点数，范围为90 ~ -90
          yPoint = res.longitude // 经度，浮点数，范围为180 ~ -180
          this.$http.post(`/list/position/`, {x_point: xPoint, y_point: yPoint}).then(res => {
          }).catch(err => console.log(err.response.data))
        }
      })
    },
    getList () {
      this.$http.get(`/list/nearby/`).then(res => {
        this.itemList = res.data
      }).catch(err => console.log(err.response.data))
    }
  }
}
</script>

<style lang="css" scoped>
.title {
  background-color: #fff;
  border-bottom: 1px solid rgba(200, 200, 200, 0.5);
}
.title-string {
  padding-left: 15px;
  font-size: 14px;
  color: #919191;
}
</style>
