<template lang="html">
  <div class="children-container">
    <div class="top-part">
      <button @click="addClick">添加</button>
    </div>
    <timeline>
      <timeline-item v-for="item in readPlan" class="time-item">
				<div class="time-item-container">
          <div class="left-part">
            <h4 class="recent">{{item.title}}</h4>
    				<p class="recent">阅读时间: {{dateFormat(item.begin_time, 'YYYY.MM.DD') + '-' + dateFormat(item.end_time, 'YYYY.MM.DD')}}</p>
  				</div>
          <div class="right-part">
            <x-button mini>删除</x-button>
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

<style lang="css">
.children-container .vux-timeline {
  padding: 10px;
}
.vux-timeline .vux-timeline-item-content {
  padding: 0 0 15px 12px;
}
.recent {
	color: rgb(4, 190, 2)
}
.time-item-container {
  display: flex;
};
.left-part, .right-part {
  flex: 1;
  text-align: center;
}
</style>
