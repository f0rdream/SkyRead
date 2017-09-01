<template lang="html">
  <div class="page-wrapper">
    <div class="card-container">
      <div class="card-title"><span class="title">新建笔记</span></div>
      <div class="book-select">
        <div class="book-box-label">所属书籍</div>
        <div class="book-box" @click="popupShow = !popupShow">
          <div class="book-text">
            {{ bookSelect[0] }}
          </div>
        </div>
        <popup-picker :show="popupShow" v-model="bookSelect" :data="[bookList]" :show-cell="false" :show-name="true"></popup-picker>
      </div>
      <div class="pic-upload">
        <label class="i-btn-blank upload-btn">拍照获取<input class="upload-input" type="file" accept="image/*" @change="onFileChange"/></label>
        <textarea class="image-result i-area" v-model="imageResult" placeholder="转换文字的内容"></textarea>
      </div>
      <div class="comment-box">
        <div class="comment-title">批注</div>
        <textarea v-model="comment" class="i-area comment-content" placeholder="写下您的批注"></textarea>
      </div>
      <div class="opt-box">
        <button @click="saveResult" class="i-btn btn-save">保存</button>
        <button @click="cancel" class="i-btn btn-cancel">放弃</button>
      </div>
    </div>
  </div>
</template>

<script>
import { PopupPicker } from 'vux'
export default {
  components: {
    PopupPicker
  },
  data () {
    return {
      popupShow: false,
      bookSelect: [],
      bookListRaw: [],
      imageResult: '',
      comment: '',
      title: ''
    }
  },
  computed: {
    bookList: function () {
      let arr = []
      for (let i of this.bookListRaw) {
        arr.push({ name: i.title, value: i.isbn13 })
      }
      return arr
    }
  },
  mounted () {
    this.getBookList()
  },
  methods: {
    onFileChange (e) {
      let files = e.target.files || e.dataTransfer.files
      if (!files.length) {
        return
      }
      let formData = new FormData()
      formData.append('image', files[0])
      this.$http.post(`/book/img2text/`, formData).then(res => {
        console.log(res)
      }).catch(err => console.log(err))
    },
    saveResult () {
      this.$http.post(`/book/note/`,
        {
          content: this.imageResult,
          isbn13: this.bookSelect[0],
          comment: this.comment
        }
      ).then(res => {
        this.$router.replace(`/note`)
      }).catch(err => console.log(err))
    },
    cancel () {
      this.$router.replace(`/note`)
    },
    getBookList () {
      this.$http.get('/book/note_list/').then(res => {
        this.bookListRaw = res.data
      })
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
.comment-title {
  font-size: 14px;
}
.comment-content {
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
</style>
