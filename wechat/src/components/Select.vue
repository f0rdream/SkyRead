<template lang="html">
  <div class="component-container">
    <div class="select-container">
      <ul class="option-box">
        <li class="title-box" @click="optionShow = !optionShow"> {{ currentItems[currentIndex].title }} </li>
        <li v-for="(item, index) in currentItems" @click="itemClick(index)" v-show="optionShow">
          {{ item.title }}
        </li>
      </ul>
    </div>
  </div>

</template>

<script>
export default {
  props: {
    items: Array
  },
  data () {
    return {
      currentItems: this.items,
      currentIndex: 0,
      optionShow: false
    }
  },
  methods: {
    itemClick (index) {
      this.currentIndex = index
      this.optionShow = !this.optionShow
      this.$emit('emitIndex', this.currentIndex)
    }
  }
}
</script>

<style lang="css" scoped>
.component-container {
  display: inline-block;
  color: #656565;
  text-align: center;
}
.select-container {
  position: relative;
  height: 30px;
}
.title-box {
  padding-bottom: 0;
}
.option-box {
  background: #fff;
  position: absolute;
  width: 100%;
}
.option-box>li {
  list-style-type: none;
  width: 100%;
  margin-top: 5px;
}
.title-box::after {
  content: '';
  width: 0;
  height: 0;
  display: inline-block;
  border-left: 8px solid transparent;
  border-bottom: 8px solid #000;
}
.triangle {
  width: 0;
  height: 0;
  border-left: 50px solid #000;
  border-bottom: 50px solid #000;
}
</style>
