<template lang="html">
  <div class="page-wrapper">
    <div class="list-card">
      <div class="card-title i-ellipsis">{{ listDetail.title }}</div>
      <div class="card-body">
        <div class="list-comment">{{ listDetail.comment }}</div>
        <div class="list-item" v-for="item in listDetail.books_info">
          <span class="book-name">{{ item.title }}</span>
          <span class="book-view" @click="$router.push(`/home/bookdetail/${item.isbn13}`)">查看</span>
        </div>
      </div>
      <div class="card-footer">
        <div class="opt-box">
          <span>评价</span>
          <span @click="addFavor">收藏</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  data () {
    return {
      listDetail: {},
      id: this.$route.params.id
    }
  },
  mounted () {
    this.getInfo()
  },
  methods: {
    ...mapActions(['setErrMsg']),
    getInfo () {
      this.$http.get(`/accounts/book_list/${this.id}/`).then(res => {
        this.listDetail = res.data
      }).catch(err => console.log(err.response.data))
    },
    addFavor () {
      this.$http.post(`/accounts/book_list/star/`, {list_id: this.id}).then(res => {
        this.setErrMsg({text: '收藏成功'})
      }).catch(err => this.setErrMsg({text: err.response.data, type: 'cancel'}))
    }
  }
}
</script>

<style lang="css" scoped>
.list-card {
  margin: .10rem .15rem;
  box-shadow: 0 0 1px 1px rgba(70, 70, 70, 0.1);
  padding: .10rem .20rem;
  background-color: #ffffdb;
}
.card-title {
  text-align: center;
  font-size: 16px;
  color: #727272;
}

.card-body {
  min-height: 2.5rem;
  overflow-y: scroll;
}
.list-comment {
  margin-bottom: .20rem;
}
.list-item, .list-comment {
  color: #727272;
  font-size: 12px;
}

.book-view {
  float: right;
  color: #4aabf6;
}
.card-footer {
  display: flex;
  flex-direction: row-reverse;
}
.opt-box {

}
</style>
