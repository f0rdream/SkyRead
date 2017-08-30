<template lang="html">
  <div class="app-wrapper">
    <div class="feedback-input-part">
      <div class="feedback-area-container">
        <textarea class="feedback-area" v-model="feedbackString"></textarea>
      </div>
      <div class="btn-container">
        <button class="i-btn i-btn-lg" @click="postComment">提交</button>
      </div>
    </div>
    <div class="feedback-display-part">
      <div class="feedback-suggest-container">
        <div class="feedback" v-for="item in feedbackList">
          <p class="feedback-username">{{ item.content }}</p>
          <p class="feedback-content">{{ item.back_content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      feedbackString: '',
      feedbackList: []
    }
  },
  mounted () {
    this.getComment()
  },
  methods: {
    getComment () {
      this.$http.get(`/accounts/feedback/`).then(res => {
        this.feedbackList = res.data
      }).catch(err => console.log(err.response.data))
    },
    postComment () {
      this.$http.post(`/accounts/feedback/`, {content: this.feedbackString}).then(res => {
        this.getComment()
      }).catch(err => console.log(err.response.data))
    }
  }
}
</script>

<style lang="css">
.feedback-area-container {
  display: flex;
  justify-content: center;
}
.feedback-area {
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
.feedback {
  background-color: #fff;
  margin: 10px 25px;
  border-radius: 8px;
  padding: 5px 10px;
}
.feedback-username {
  font-size: 16px;
}
.feedback-content {
  font-size: 12px;
}
</style>
