<template lang="html">
  <div class="app-wrapper">
    <div class="comment-input-part">
      <textarea></textarea>
      <div class="btn-container">
        <button class="i-btn i-btn-lg">提交</button>
      </div>
    </div>
    <div class="comment-display-part">
      <div class="comment-suggest-container">
        <div class="comment-suggest">
          <p class="comment-username">{{ doubanComment.author }}</p>
          <p class="comment-content">{{ doubanComment.content }}</p>
        </div>
      </div>
      <div class="comment-normal-container">
        <div class="comment-nornmal" v-for="item in normalComment">
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
      doubanComment: {
        author: '',
        content: ''
      },
      normalComment: []
    }
  },
  mounted () {
    this.getDouban()
    this.getNormal()
  },
  methods: {
    getDouban () {
      this.$http.get(`/douban/comments/${this.$route.params.isbn13}/`).then(res => {
        this.doubanComment = {...this.doubanComment, ...res.data[0]}
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
      }).catch(err => console.log(err))
    }
  }
}
</script>

<style lang="css">
</style>
