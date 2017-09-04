<template lang="html">
  <div class="children-container">
    <div v-for="item in readPlan" class="time-item card" :key="item.id">
      <div class="delete-box" @click="delReadPlan(item.id)"><i class="i-icon-cross i-icon-plus"></i></div>
			<div class="item-outer">
        <div class="left-part">
          <h4 class="item-info">{{item.title}}</h4>
  				<p class="item-info">开始日期: {{dateFormat(item.begin_time, 'YYYY-MM-DD')}}</p>
          <p class="item-info">结束日期: {{dateFormat(item.end_time, 'YYYY-MM-DD')}}</p>
				</div>
        <div class="right-part">
          <button class="i-btn" @click="$router.push(`/bookshelf/signin/${item.id}`)">打卡</button>
        </div>
			</div>
      <div class="bar-container">
        <div class="bar">
          <div class="bar-inner" :style="{width: `${(item.now_page / item.sum_page) * 100}%`}"></div>
        </div>
      </div>
		</div>

    <div class="spinner-rb spinner" @click="addClick">
      <i class="i-icon-plus"></i>
    </div>
  </div>
</template>

<script>
import { dateFormat, XButton } from 'vux'
import { mapGetters, mapActions } from 'vuex'

export default {
  components: {
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
      'getReadPlan',
      'delReadPlan'
    ]),
    dateFormat,
    addClick () {
      this.$router.push('/addplan')
    }
  }
}
</script>

<style lang="css" scoped>
.card {
  position: relative;
  background-color: #fff;
  margin: .10rem .15rem;
  box-shadow: 0 1px 1px 1px rgba(50, 50, 50, 0.1);
  border-radius: 5px;
  padding: .10rem .15rem;
}
.delete-box {
  position: absolute;
  top: 0px;
  right: 0px;
  transform: scale(0.75);
}
.i-icon-cross {
  transform: rotate(45deg);
  color: #777;
}
.i-icon-cross:active {
  color: #aaa;
}

.item-info {
  color: #767676;
  font-size: 14px;
}
.item-outer {
  display: flex;
}
.left-part {
  flex: 1 1 auto;
}
.right-part {
  flex-grow: 0;
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-right: 8px;
}
.right-part .i-btn {
  background-color: #25d398;
}
.right-part .i-btn:active {
  background-color: #63d5ae;
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

.spinner {
  position: fixed;
  width: 40px;
  height: 40px;
  background: #25d398;
  border-radius: 50%;
  display: flex;
}
.spinner:active {
  background: #64d3ad;
}
.spinner>i {
  margin: auto;
}
.spinner-rb {
  bottom: 70px;
  right: 20px;
}



</style>
