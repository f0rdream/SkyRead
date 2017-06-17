import { SET_WECHATSIGN, SET_BORROWQRINFO, SET_SCANEDCART, DEL_SCANEDCART } from './mutation-types'

export default {
  [SET_WECHATSIGN] (state, sign) {
    state.wechatSign = sign
  },
  [SET_BORROWQRINFO] (state, payload) {
    state.borrowQRInfo = payload
  },
  [SET_SCANEDCART] (state, payload) {
    state.scanedCart = payload
  },
  [DEL_SCANEDCART] (state, index) {
    state.scanedCart.splice(index, 1)
  }
}
