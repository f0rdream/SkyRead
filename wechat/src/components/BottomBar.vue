<template>
  <div class="bar-wrapper">
    <div class="bottom-item" :class="getBarStyle(index)" @click="tabBarLink(index)" v-for="(item, index) in currentTabs">
      <img :src="index === activeTab ? item.cImg : item.img" class="bottom-icon">
      <div class="bottom-text">{{currentTabs[index].name}}</div>
    </div>
    <div class="bar-center" @click="scanQR">
      <img src="/static/others/brush.png" class="bottom-center-icon">
    </div>
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
          url: '/home/indexpage',
          img: '/static/bottom/home.png',
          cImg: '/static/bottom/home_c.png'
        },
        {
          name: '搜索',
          url: '/search',
          img: '/static/bottom/search.png',
          cImg: '/static/bottom/search_c.png'
        },
        {
          name: '书架',
          url: '/bookshelf/scaned',
          img: '/static/bottom/bookshelf.png',
          cImg: '/static/bottom/bookshelf_c.png'
        },
        {
          name: '个人',
          url: '/person',
          img: '/static/bottom/person.png',
          cImg: '/static/bottom/person_c.png'
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
            vueThis.setErrMsg({text: '扫码成功'})
          }).catch(err => {
            vueThis.setErrMsg({text: err.response.data, type: 'cancel'})
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
      'getScanedList',
      'setErrMsg'
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
  z-index: 100;
}
.bar-wrapper .active {
  color: #2bc3c2;
}
.bar-wrapper>div:not(.bar-center) {
  padding-top: 8px;
  width: 25%;
  text-align: center;
  font-size: 10px;
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
  width: 68px;
  position: absolute;
  left: 50%;
  bottom: 0;
  transform: translateX(-50%);
  border-radius: 50%;
  text-align: center;
  box-shadow: 0 0 5px #2bc0cb;
  display: flex;
  justify-content: center;
  align-items: center;
}
.bottom-center-icon {
  height: 40px;
  width: 40px;
}

.bottom-icon {
  height: 25px;
  width: 25px;
}
.botton-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
