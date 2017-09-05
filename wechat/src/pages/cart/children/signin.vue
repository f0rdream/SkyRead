<template lang="html">
  <div class="page-wrapper">
    <div class="card">
      <div class="card-title">
        读书打卡
        <div class="sign-box" @click="showSign = !showSign">
          <span class="sign-icon">签</span>
        </div>
      </div>
      <div class="book-card">
        <div class="book-body">
          <div class="left">
            <img :src="getImg(planDetail.img_id)" class="book-img">
          </div>
          <div class="right">
            <p class="body-title"> {{ planDetail.title }}</p>
            <p class="body-info author">作者：<span v-for="item in planDetail.author">{{ item }}</span></p>
            <p class="body-info">页数：{{ planDetail.sum_page }}</p>
            <p class="body-info">开始时间：{{ dateFormat(timePY2JS(planDetail.begin_time), 'YYYY-MM-DD') }}</p>
            <p class="body-info">出版时间：{{ dateFormat(timePY2JS(planDetail.end_time), 'YYYY-MM-DD') }}</p>
          </div>
        </div>
        <div class="progress-box">
          当前阅读进度
          <div class="bar">
            <div class="bar-inner" :style="{width: `${(planDetail.now_page / planDetail.sum_page) * 100}%`}"></div>
          </div>
        </div>
      </div>
      <div class="calendar-box">
        <inline-calendar :render-function="customDate" :return-six-rows="false" v-model="dateValue">
          <template scope="props" slot="each-day">
            <div class="day-container" :class="customDate(props.rawDate)">
               <span class="day-span">{{props.child.day}}</span>
            </div>
          </template>
        </inline-calendar>
      </div>
    </div>
    <div v-transfer-dom>
      <x-dialog v-model="showSign" :hide-on-blur="true">
        <div class="modal-container">
          <div class="modal-title">今日打卡</div>
          <div class="modal-body">
            <label class="modal-text">本次读到<input type="number" v-model="now_page" class="modal-input"></label>
          </div>
          <div class="modal-footer">
            <button class="i-btn" @click="signOK">确定</button>
          </div>
        </div>
      </x-dialog>
      <x-dialog v-model="showSigned" :hide-on-blur="true">
        <div class="modal-container">
          <div class="modal-title">打卡记录</div>
          <div class="modal-body">
            在{{planDayDetail.record_date}}这一天，您从 P{{planDayDetail.last_page}} 读到了 P{{planDayDetail.now_page}} ，请您继续加油，再接再厉!
          </div>
          <div class="modal-footer">
            <button class="i-btn" @click="signedOK">确定</button>
          </div>
        </div>
      </x-dialog>
    </div>
  </div>
</template>

<script>
import { timePY2JS } from '@/config/utils'
import { InlineCalendar, dateFormat, XDialog, TransferDomDirective as TransferDom } from 'vux'
export default {
  components: {
    InlineCalendar,
    XDialog
  },
  directives: {
    TransferDom
  },
  data () {
    return {
      planDetail: {},
      id: this.$route.params.id,
      signedDays: [],
      showSign: false,
      showSigned: false,
      now_page: 0,
      dateValue: '',
      planDayDetail: {}
    }
  },
  mounted () {
    this.getPlan()
    this.getSum()
  },
  watch: {
    dateValue (newDate) {
      if (this.signedDays.indexOf(newDate) !== -1) {
        this.$http.get(`/book/record/${this.id}?date=${this.dateFormat(newDate, 'YYYY-MM-DD')}`).then(res => {
          this.planDayDetail = res.data
          this.showSigned = !this.showSigned
        })
      }
    }
  },
  methods: {
    getPlan () {
      this.id = this.$route.params.id
      this.$http.get(`/book/readplan/${this.id}`).then(res => {
        this.planDetail = res.data
      }).catch(err => console.log(err.response.data))
    },
    getSum () {
      this.$http.get(`/book/record/sum/${this.id}`).then(res => {
        this.signedDays = res.data
      }).catch(err => console.log(err.response.data))
    },
    customDate (rawDate) {
      return this.signedDays.indexOf(rawDate) !== -1 ? 'signed' : ''
    },
    getImg (imgId) {
      return imgId ? `https://img3.doubanio.com/lpic/${imgId}` : null
    },
    signOK () {
      this.$http.post(`/book/record/${this.id}`, {now_page: this.now_page}).then(res => {
        this.getPlan()
        this.showSign = !this.showSign
      }).catch(err => console.log(err.response.data))
    },
    signedOK () {
      this.showSigned = !this.showSigned
    },
    dateFormat,
    timePY2JS
  }
}
</script>

<style lang="css" scoped>
.card {
  margin: .10rem .10rem;
  background: #fff;
  overflow: hidden;
  border-radius: 5px;
  box-shadow: 0 0 1px 1px rgba(70, 70, 70, 0.1);
}
.card-title {
  margin-top: .10rem;
  position: relative;
  text-align: center;
  font-size: 18px;
  color: #636363;
}
.book-card {
  background-color: #fff;
  padding: .10rem .10rem;
}
.book-body {
  display: flex;
  padding: .15rem .05rem;
  padding-bottom: 0;
  color: #636363;
}
.book-body>.left {
  flex: 0 0 35%;
  text-align: center;
}
.book-img {
  width: 80%;
}
.book-body>.right {
  flex: 1 1 auto;
  padding-left: .05rem;
}
.body-title {
  font-size: 14px;
  margin-bottom: .10rem;
}
.body-info {
  font-size: 13px;
}
.body-info.author {
  white-space: normal;
}
.sign-box {
  position: absolute;
  right: .10rem;
  top: 0;
  height: 36px;
  width: 36px;
  border-radius: 50%;
  display: inline-flex;
  border: 1px solid #000;
  border-radius: 50%;
  line-height: 1;
}
.sign-icon {
  margin: auto;
}

.progress-box {
  text-align: center;
  font-size: 14px;
  color: #717171;
  margin-top: .05rem;
  padding: 0 .15rem;
}
.bar {
  height: 10px;
  border: 1px solid #25d398;
  margin-top: .05rem;
}
.bar, .bar-inner{
  border-radius: 5px;
}
.bar-inner {
  height: 100%;
  background-color: #25d398;
}

.modal-container {
  padding: .15rem;
  color: #636363;
}
.modal-title {
  font-size: 16px;
  margin: .05rem 0 .10rem 0;
}
.modal-text {
  font-size: 14px;
  padding: .05rem .10rem;
}
.calendar-box {
  margin-top: .15rem;
}
.modal-input {
  margin-left: .10rem;
}
.modal-footer {
  margin-top: .16rem;
}

.day-container {
    display: inline-flex;
    width: 25px;
    height: 25px;
}
.signed {
  background-color: #29d798;
  color: #fff;
  border-radius: 50%;
}
.day-span {
  display: inline-block;
  margin: auto;
}



</style>
