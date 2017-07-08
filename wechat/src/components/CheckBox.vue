<template lang="html">
  <label class="i-checker-container" type="checkbox">
    <input type="checkbox" class="i-checker-input" v-model="checkValue" :value="value">
    <i class="i-checker-icon"></i>
  </label>
</template>

<script>
export default {
  model: {
    prop: 'checked'
  },
  // props: {
  //   value: String
  // },
  props: [
    'checked',
    'value'
  ],
  computed: {
    checkValue: {
      get () {
        return this.checked
      },
      set (val) {
        this.$emit('input', val)
      }
    }
  }
}
</script>

<style lang="css" scoped>
</style>
