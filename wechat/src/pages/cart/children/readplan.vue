<template lang="html">
  <div class="children-container">
    <div class="top-part">
      <button @click="addClick" class="i-btn-round"><i class="round-add"></i></button>
    </div>
    <timeline>
      <timeline-item v-for="item in readPlan" class="time-item" :key="item.id">
				<div class="time-item-container">
          <div class="left-part">
            <h4 class="item-info">{{item.title}}</h4>
    				<p class="item-info">阅读时间: {{dateFormat(item.begin_time, 'YYYY.MM.DD') + '-' + dateFormat(item.end_time, 'YYYY.MM.DD')}}</p>
  				</div>
          <div class="right-part">
            <button class="i-btn">删除</button>
          </div>
				</div>
			</timeline-item>
    </timeline>
  </div>
</template>

<script>
import { Timeline, TimelineItem, dateFormat, XButton } from 'vux'
import { mapGetters, mapActions } from 'vuex'

export default {
  components: {
    Timeline,
    TimelineItem,
    XButton
  },
  data () {
    return {
    }
  },
  computed: {
    ...mapGetters({
      readPlan: 'readPlanGetter'
    })
  },
  mounted () {
    this.getReadPlan()
  },
  methods: {
    ...mapActions([
      'getReadPlan'
    ]),
    dateFormat,
    addClick () {
      this.$router.push('/addplan')
    }
  }
}
</script>

<style lang="css" scoped>
.children-container {
  background-color: #fbfbfb;
}
.top-part .i-btn-round{
  margin-left: 8px;
  margin-top: 8px;
}
.children-container .vux-timeline {
  padding: 15px;
}
.vux-timeline .vux-timeline-item-content {
  padding: 8px 0 25px 30px;
}
.item-info {
  color: #676767;
  font-size: 14px;
}
/*.item-info {
	color: rgb(4, 190, 2);
}*/
.time-item-container {
  display: flex;
};
.left-part {
  flex: 1;
}
.right-part {
  flex-grow: 0;
  flex-shrink: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-right: 8px;
}

.i-btn-round {
  border: 0;
  border-radius: 50%;
  outline: 0;
  background-color: rgba(255, 255, 255, 0)
}
.round-add {
  display: inline-block;
  position: relative;
  border: 0;
  height: 30px;
  width: 30px;
  border-radius: 50%;
  background-color: #279f95;
}
.round-add::before, .round-add::after {
  display: inline-block;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  content: '';
  background-color: #fff;
}
.round-add::after {
  height: 20px;
  width: 3px;
}
.round-add::before {
  width: 20px;
  height: 3px;
}
</style>
