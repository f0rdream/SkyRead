import { SET_WECHATSIGN } from './mutation-types'

export default {
  setWechatSign ({commit, state}) {
    let url = window.location.href.split('#')[0]
    this.$http.get('url', url).then(res => {
      commit(SET_WECHATSIGN, res)
    }).catch(err => {
      console.err(err)
    })
  }
}
