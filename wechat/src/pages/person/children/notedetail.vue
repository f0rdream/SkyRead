<template lang="html">
  <div class="page-wrapper">
    <div class="item-container">
      <div class="book-part">
        <div class="item-title">{{noteDetail.title}}</div>
        <div class="item-content">{{noteDetail.content}}</div>
      </div>
      <div class="item-comment">{{noteDetail.comment}}</div>
      <div class="item-opt">
        <div class="time">{{noteDetail.date}}</div>
        <div class="opt-box">
          <span @click="delNote(noteDetail.id)">删除</span>
          <span @click="modNote(noteDetail.id)">修改</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      noteId: '',
      noteDetail: {}
    }
  },
  mounted () {
    this.getInfo()
  },
  methods: {
    getInfo () {
      this.noteId = this.$route.params.id
      this.$http.get(`/book/note/${this.noteId}`).then(res => {
        this.noteDetail = res.data
      }).catch(err => console.log(err))
    },
    getNotes () {
      this.$http.get(`/book/note/`).then(res => {
        this.noteList = res.data
      }).catch(err => console.log(err))
    },
    delNote (id) {
      this.$http.delete(`/book/note/${id}`).then(res => {
        this.getNotes()
      }).catch(err => console.log(err))
    },
    modNote (id) {
      this.$router.push('/modnote')
    }
  }
}
</script>

<style lang="css" scoped>
.item-container {
  margin: .10rem .15rem;
  background-color: #fff8ac;
  border-radius: 10px;
  overflow: hidden;
}
.book-part {
  background-color: #fff;
  margin: .15rem .20rem .15rem .10rem;
  padding: .05rem 0 .10rem .20rem;
}
.item-title {
  border-bottom: 1px solid #d5d5d5;
  padding: .02rem 0.08rem;
}
.item-content {
  padding: .05rem 0.08rem;
  font-size: 14px;
  color: #6b6b6b;
}
.item-comment {
  color: #6b6b6b;
  font-size: 14px;
  padding: 0 .25rem;
}
.item-opt {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  padding: .20rem .25rem .10rem .25rem;
  color: #6b6b6b;
}
.opt-box {
  font-size: 12px;
}
</style>
