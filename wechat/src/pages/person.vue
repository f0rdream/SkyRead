<template>
  <div class="app-wrapper">
    <x-header :right-options="{showMore: true}">个人信息</x-header>
    <section class="avatar-part">
      <img class="avatar" src="../assets/logo.png">
      <p class="avatar-info">{{ username }}</p>
    </section>
    <section class="book-part">
      <clickable-list :books="books" labelText="想读的书"></clickable-list>
    </section>
  </div>
</template>
<script>
import { XHeader } from 'vux'
import ClickableList from '../components/ClickableList'

export default {
  components: {
    XHeader,
    ClickableList
  },
  data () {
    return {
      username: '微信名字',
      books: ['1', '1', '1']
    }
  }
}
</script>
<style scoped>
.avatar-part {
  text-align: center;
  height: 1.7rem;
}
.avatar {
  margin-top: .15rem;
  height: 1rem;
  width: 1rem;
  border-radius: 50% 50%;
}
</style>
