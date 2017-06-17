import Vue from 'vue'
import Vuex from 'vuex'
import mutations from './mutations'
import actions from './actions'
import getters from './getters'
import '../config/ajax'

Vue.use(Vuex)

const state = {
  wechatSign: '',
  favoraite: [],
  scanedCart: [],
  rentingCart: [],
  rentedHistory: [],
  borrowQRInfo: {}
}
export default new Vuex.Store({
  state,
  getters,
  actions,
  mutations
})
