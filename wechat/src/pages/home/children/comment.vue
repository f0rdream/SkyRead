<template lang="html">
  <div class="app-wrapper">
    <div class="comment-input-part">
      <div class="comment-area-container">
        <textarea class="comment-area" v-model="commentString"></textarea>
      </div>
      <div class="btn-container">
        <button class="i-btn i-btn-lg" @click="postComment">提交</button>
      </div>
    </div>
    <div class="comment-display-part">
      <div class="comment-suggest-container">
        <div class="comment" v-for="item in doubanComment">
          <p class="comment-username">{{ item.author }}</p>
          <p class="comment-content">{{ item.content }}</p>
        </div>
      </div>
      <div class="comment-normal-container">
        <div class="comment" v-for="item in normalComment">
          <p class="comment-username">{{ item.nickname }}</p>
          <p class="comment-content">{{ item.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      commentString: '',
      doubanComment: [],
      normalComment: []
    }
  },
  mounted () {
    this.getNormal()
    this.getDouban()
  },
  methods: {
    getDouban () {
      this.$http.get(`/douban/comments/${this.$route.params.isbn13}/`).then(res => {
        this.doubanComment = res.data
      }).catch(err => console.log(err))
    },
    getNormal () {
      this.$http.get(`/book/comments/${this.$route.params.isbn13}/`).then(res => {
        this.normalComment = res.data
      }).catch(err => console.log(err))
    },
    postComment () {
      this.$http.post(`/book/comments/${this.$route.params.isbn13}/`, {content: this.commentString}).then(res => {
        this.normalComment = res.data
        this.getNormal()
      }).catch(err => console.log(err))
    }
  }
}
</script>

<style lang="css">
.comment-area-container {
  display: flex;
  justify-content: center;
}
.comment-area {
  margin-top: 20px;
  height: 100px;
  width: 100%;
  margin: 20px 25px 10px 25px;
  border: 1px solid rgba(200, 200, 200, 0.6);
  outline: none;
  border-radius: 8px;
  font-size: 14px;
  padding: 15px 20px;
  resize: none;
}
.comment {
  background-color: #fff;
  margin: 10px 25px;
  border-radius: 8px;
  padding: 5px 10px;
}
.comment-username {
  font-size: 16px;
}
.comment-content {
  font-size: 12px;
}
</style>
