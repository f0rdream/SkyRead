import { SET_WECHATSIGN, SET_QRINFO, SET_SCANEDCART, DEL_SCANEDCART, SET_RENTINGCART, SET_FAVROITES, ADD_FAVROITES, SET_ERRORMSG, SET_ORDEREDCART, SET_READPLAN, SET_ACCOUNTSINFO, SET_HAVEPHONE, SET_CURRENTTAB } from './mutation-types'

export default {
  [SET_ERRORMSG] (state, payload) {
    state.errorMsg = {...{type: 'success'}, ...payload}
  },
  [SET_WECHATSIGN] (state, sign) {
    state.wechatSign = sign
  },
  [SET_QRINFO] (state, payload) {
    state.QRInfo = payload
  },
  [SET_SCANEDCART] (state, payload) {
    state.scanedCart = payload
  },
  [DEL_SCANEDCART] (state, index) {
    state.scanedCart.splice(index, 1)
  },
  [SET_RENTINGCART] (state, payload) {
    state.rentingCart = payload
  },
  [SET_FAVROITES] (state, payload) {
    state.favorite = payload
  },
  [ADD_FAVROITES] (state, payload) {
    state.favorite += payload
  },
  [SET_ORDEREDCART] (state, payload) {
    state.orderedCart = payload
  },
  [SET_READPLAN] (state, payload) {
    state.readPlan = payload
  },
  [SET_ACCOUNTSINFO] (state, payload) {
    state.accountsInfo = payload
  },
  [SET_HAVEPHONE] (state, payload) {
    state.havePhone = payload
  },
  [SET_CURRENTTAB] (state, payload) {
    state.currentTab = payload
  }
}
