import { SET_WECHATSIGN } from './mutation-types'

export default {
  [SET_WECHATSIGN] (state, sign) {
    state.wechatSign = sign
  }
}
