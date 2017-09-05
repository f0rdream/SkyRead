import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import actions from './actions'
import getters from './getters'
import '../config/ajax'

Vue.use(Vuex)

const state = {
  scanedMax: 2,     // Define the max amount in the scanedCart
  errorMsg: {text: '', type: ''},
  wechatSign: '',
  favorite: [],
  scanedCart: [],
  rentingCart: [],
  rentedHistory: [],
  orderedCart: {},
  readPlan: [],
  QRInfo: {},
  accountsInfo: {},
  havePhone: true,
  currentTab: 0,
  tempBookList: []
}
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
