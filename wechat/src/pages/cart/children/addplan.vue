<template lang="html">
  <div class="children-container">
    <group>
      <popup-picker :data="[favorList]" v-model="checkedBook" title="选择书籍" placeholder="请选择" :show-name="true"></popup-picker>
    </group>
    <group title="选择时间">
      <datetime :title="'开始时间'" v-model="beginTime" :start-date="todayString"></datetime>
      <datetime :title="'结束时间'" v-model="endTime" :start-date="beginTime"></datetime>
    </group>
    <div class="btn-container">
      <button class="i-btn" @click="submit">提交</button>
    </div>
  </div>
</template>

<script>
import { Cell, PopupPicker, Group, Datetime, XButton } from 'vux'
import { mapGetters, mapActions } from 'vuex'
import { timeJS2PY } from '@/config/utils'

export default {
  components: {
    Cell,
    PopupPicker,
    Group,
    Datetime,
    XButton
  },
  data () {
    return {
      checkedBook: [],
      beginTime: '',
      endTime: ''
    }
  },
  computed: {
    ...mapGetters({
      favorList: 'favoriteList'
    }),
    todayString () {
      let today = new Date()
      return `${today.getFullYear()}-${today.getMonth() + 1}-${today.getDate()}`
    }
  },
  mounted () {
    this.getFavorite()
  },
  methods: {
    ...mapActions({
      getFavorite: 'getFavorite',
      setErrMsg: 'setErrMsg'
    }),
    submit () {
      // let begin_time = timeJS2PY(this.beginTime)
      // let end_time = timeJS2PY(this.endTime)
      let form = {isbn13: this.checkedBook[0], begin_time: timeJS2PY(this.beginTime), end_time: timeJS2PY(this.endTime)}
      this.$http.post('/book/readplan/', form).then(res => {
        this.setErrMsg({text: '信息更新成功'})
        setTimeout(() => {
          this.$router.go(-1)
        }, 2000)
      }).catch(err => this.setErrMsg({text: err.response.data, type: 'cancel'}))
    }
  }
}
</script>

<style lang="css">
.btn-container {
  margin: 10px;
  display: flex;
  justify-content: center;
}
</style>
