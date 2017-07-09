import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import actions from './actions'
import getters from './getters'
import '../config/ajax'

Vue.use(Vuex)

const state = {
  errorMsg: '',
  wechatSign: '',
  favorite: [],
  scanedCart: [],
  rentingCart: [],
  rentedHistory: [],
  orderedCart: {},
  readPlan: [],
  QRInfo: {},
  accountsInfo: {},
  havePhone: true
}
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
