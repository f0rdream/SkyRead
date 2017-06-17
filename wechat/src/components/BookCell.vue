<template lang="html">
  <div class="cell-container">
    <div class="left">
      <slot class="book-title" name="book-title"></slot>
      <slot class="book-info" name="book-info"></slot>
    </div>
    <div class="right">
      <slot name="right"></slot>
    </div>
  </div>
</template>

<script>
export default {
}
</script>

<style lang="css">
.cell-container {
  display: flex;
  justify-content: space-between;
  padding: 8px 25px 15px 25px;
  background-color: #fff;
}
.book-title {
  font-size: 12px;
}
.book-info {
  color: #787878;
  font-size: 10px;
}
</style>
