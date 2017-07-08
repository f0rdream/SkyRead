<template lang="html">
  <div class="cell-container">
    <div class="left">
      <div class="checker-slot-container" v-if="slotExists('book-checker')">
        <slot class="book-checker" name="book-checker"></slot>
      </div>
      <div class="info-slot-container">
        <slot class="book-title" name="book-title"></slot>
        <slot class="book-info" name="book-info"></slot>
      </div>
    </div>
    <div class="right">
      <slot name="right"></slot>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    slotExists (slotName) {
      return this.$slots[slotName]
    }
  }
}
</script>

<style lang="css" scoped>
.cell-container {
  display: flex;
  justify-content: space-between;
  padding: 8px 15px 15px 15px;
  background-color: #fff;
}
.book-title {
  font-size: 13px;
}
.book-info {
  color: #787878;
  font-size: 10px;
}
.left {
  display: flex;
  flex-grow: 1;
}
.checker-slot-container {
  flex-grow: 0;
  flex-basis: 25px;
  display: flex;
  align-items: center;
  margin-right: 10px;
}
.info-slot-container {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  flex-direction: column;
}
.right {
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  justify-content: center;
}
</style>
