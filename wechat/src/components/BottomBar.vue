<template>
  <div class="bar-wrapper">
    <div :class="getBarStyle(index)" @click="tabBarLink(index)" v-for="(item, index) in currentTabs">{{currentTabs[index].name}}</div>
    <!-- <div :class="activeTab === currentTabs[0].name ? 'active' : ''" @click="$router.replace(currentTabs[0].url)">{{currentTabs[0].name}}</div>
    <div class="bar-left" :class="activeTab === currentTabs[1].name ? 'active' : ''" @click="$router.replace(currentTabs[1].url)">{{currentTabs[1].name}}</div>
    <div class="bar-right" :class="activeTab === currentTabs[2].name ? 'active' : ''" @click="$router.replace(currentTabs[2].url)">{{currentTabs[2].name}}</div>
    <div :class="activeTab === currentTabs[3].name ? 'active' : ''" @click="$router.replace(currentTabs[3].url)">{{currentTabs[3].name}}</div> -->
    <div class="bar-center" @click="scanQR">扫码借书</div>
  </div>
</template>
<script>
import { mapActions } from 'vuex'
import { querystring } from 'vux'
export default {
  props: {
    activeTab: Number,
    tabs: Array
  },
  data () {
    return {
      qrResult: {}
    }
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
          url: '/bookshelf/scaned'
        },
        {
          name: '个人',
          url: '/person'
        }
      ]
      return this.tabs || defaultTabs
    }
  },
  mounted () {
  },
  methods: {
    test () {
      let qrResult
      let qrQuery = querystring.parse('isbn13=9787111251217&id=399126&title=编译原理')
      qrResult = {book_id: qrQuery.id, isbn13: qrQuery.isbn13}
      this.$http.post('/library/borrow/', qrResult).then(res => {
        alert(res)
      }).catch(err => {
        alert('err ' + err)
      })
    },
    scanQR () {
      // TODO 提交mutation的方式提交请求
      let vueThis = this
      this.$wechat.scanQRCode({
        needResult: 1, // 默认为0，扫描结果由微信处理，1则直接返回扫描结果，
        scanType: ['qrCode', 'barCode'], // 可以指定扫二维码还是一维码，默认二者都有
        success: function (res) {
          let qrResult
          let qrQuery = querystring.parse(res.resultStr)
          qrResult = {book_id: qrQuery.id, isbn13: qrQuery.isbn13} // 当needResult 为 1 时，扫码返回的结果
          vueThis.$http.post('/library/borrow/', qrResult).then(res => {
            vueThis.getScanedList()
          }).catch(err => {
            this.$vux.alert.show({
              title: 'Error',
              content: err
            })
          })
        }
      })
    },
    getBarStyle (index) {
      let returnClass = ''
      if (index === this.activeTab) {
        returnClass = 'active'
      }
      if (index === 1) {
        returnClass += ' bar-left'
      } else if (index === 2) {
        returnClass += ' bar-right'
      }
      return returnClass
    },
    tabBarLink (index) {
      if (index !== this.activeTab) {
        this.$router.replace(this.currentTabs[index].url)
      }
    },
    ...mapActions([
      'getScanedList'
    ])
  }
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
  box-shadow: 1px -1px 1px #ccc;
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
