<template lang="html">
  <div class="page-wrapper">
    <div class="card-container">
      <div class="card-title"><span class="title">新建书单</span></div>
      <div class="book-select">
        <div class="book-box-label">标题</div>
        <div class="book-box">
          <input type="text" v-model="listTitle" class="title-input">
        </div>
      </div>
      <div class="description-box">
        <textarea v-model="description" class="i-area description-content" placeholder="请写下书单描述"></textarea>
      </div>
      <div class="book-list-container">
        <div class="book-list-item" v-for="(item, index) in tempBookList">
          <span class="item-title">{{item.title}}</span>
          <div @click="delTempBookList(index)" class="i-icon-container"><i class="i-icon-cross"></i></div>
        </div>
        <div class="new-box" @click="$router.replace('/booklistsearch')">
          <div class="i-icon-container"><i class="i-icon-plus"></i></div>
        </div>
      </div>
      <div class="opt-box">
        <button @click="saveResult" class="i-btn btn-save">保存</button>
        <button @click="cancel" class="i-btn btn-cancel">放弃</button>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState, mapActions } from 'vuex'
import { PopupPicker } from 'vux'
export default {
  components: {
    PopupPicker
  },
  data () {
    return {
      listTitle: '',
      description: ''
    }
  },
  computed: {
    isbn13List: function () {
      let arr = []
      for (let i of this.tempBookList) {
        arr.push(i.isbn13)
      }
      return arr
    },
    ...mapState({
      tempBookList: 'tempBookList'
    })
  },
  mounted () {
  },
  methods: {
    ...mapActions({
      addTempBooklist: 'addTempBooklist',
      delTempBookList: 'delTempBookList',
      setErrMsg: 'setErrMsg'
    }),
    saveResult () {
      this.$http.post(`/accounts/book_list/`,
        {
          title: this.listTitle,
          comment: this.description,
          isbn13_list: this.isbn13List
        }
      ).then(res => {
        this.setErrMsg({text: '添加成功'})
        this.$router.replace(`/booklist`)
      }).catch(err => console.log(err.response.data))
    },
    cancel () {
      this.$router.replace(`/booklist`)
    }
  }
}
</script>

<style lang="css" scoped>
.card-container {
  background-color: #fff;
  border-radius: 5px;
  margin: .20rem .10rem;
  color: #727272;
  padding: .05rem .20rem;
  box-shadow: 0 0 2px 1px rgba(0, 0, 0, 0.1);
}
.card-container>div {
  margin-top: .08rem;
}
.card-title {
  padding-top: .05rem;
  text-align: center;
  font-size: 16px;
  color: #727272;
}
.card-title>.title {
  display: inline-block;
  padding: 0rem .40rem;
  border-bottom: 1px solid #e2e2e2;
}
.book-select {
  display: flex;
}
.book-box-label {
  font-size: 14px;
  flex: 0 0 auto;
}
.book-box {
  flex: 1 1 auto;
  display: inline-block;
  border-bottom: 1px solid #e2e2e2;
  margin: 0 .25rem;
}
.title-input {
  width: 100%;
  border: 0;
  outline: none;
}
.book-text {
  text-align: center;
}
.pic-upload {

}
.upload-input {
  display: none;
}
.upload-btn {
  border: 1px #dadada solid;
  font-size: 12px;
  padding: .10rem .15rem;
}
.image-result {
  display: block;
  margin-top: .12rem;
  width: 100%;
  font-size: 14px;
  min-height: 1.2rem;
}
.card-container .description-box {
  margin-top: .15rem;
}
.description-title {
  font-size: 14px;
}
.description-content {
  width: 100%;
  min-height: 1.2rem;
}
.opt-box {
  display: flex;
  justify-content: space-around;
  padding: .05rem .05rem .15rem .05rem;
}
.btn-save {
  background-color: #25d398;
}
.btn-save:active {
  background-color: #64dbb3;
}
.btn-cancel {
  background-color: #ea4747;
}
.btn-cancel:active {
  background-color: #d96a6a;
}

.book-list-item .i-icon-container {
  float: right;
}
.i-icon-container {
  transform: scale(0.5);
  vertical-align: middle;
}
.i-icon-cross {
  color: #000;
}
.i-icon-plus {
  color: #000;
}

.item-title {
  font-size: 14px;
  vertical-align: middle;
}
.new-box {
  margin-top: .08rem;
}
</style>
