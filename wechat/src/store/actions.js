import Vue from 'vue'
import store from './index'
import { SET_ERRORMSG, SET_WECHATSIGN, SET_QRINFO, SET_SCANEDCART, SET_RENTINGCART, SET_FAVROITES, SET_READPLAN } from './mutation-types'
import '../config/ajax'
import Router from '../router/index'

export default {
  setWechatSign ({commit, state}) {
    let url = window.location.href.split('#')[0]
    this.$http.get('url', url).then(res => {
      commit(SET_WECHATSIGN, res.data)
    }).catch(err => {
      console.err(err)
    })
  },
  setErrMsg ({ commit }, msg) {
    commit(SET_ERRORMSG, msg)
  },
  getBorrowQR ({ commit, state }, indexList) {
    Vue.http.post('/library/borrow/qrcode/', {id_list: indexList}).then(res => {
      commit(SET_QRINFO, res.data)
      Router.push('/bookshelf/paying')
    })
  },
  getScanedList ({ commit }) {
    Vue.http.get('/library/borrow/').then(res => {
      commit(SET_SCANEDCART, res.data)
    }).catch(err => {
      console.log(err)
    })
  },
  delScanedList ({commit}, itemId, index) {
    Vue.http.delete(`/library/borrow/${itemId}`).then(res => {
      commit(SET_SCANEDCART, index)
    }).catch(err => {
      console.log(err)
    })
  },
  getRentingList ({ commit }) {
    Vue.http.get('/library/return/').then(res => {
      commit(SET_RENTINGCART, res.data)
    }).catch(err => {
      console.log(err)
    })
  },
  getRentingQR ({ commit, state }, indexList) {
    // let idList
    // for (let index of indexList) {
    //   idList.push(state.rentingCart[index].id)
    // }
    Vue.http.post('/library/return/qrcode/', {id_list: indexList}).then(res => {
      commit(SET_QRINFO, res.data)
      Router.push('/bookshelf/paying')
    })
  },
  getFavorite ({ commit }) {
    Vue.http.get('/book/starbook/').then(res => {
      commit(SET_FAVROITES, res.data)
    }).catch(err => {
      console.log(err)
    })
  },
  addFavorite ({ commit }, isbn13) {
    Vue.http.post('/book/starbook/', { isbn13 }).then(res => {
      res = res.data
      if (res.error_code === 0) {
        commit(SET_ERRORMSG, '加入成功')
      } else if (res.error_code === 98) {
        commit(SET_ERRORMSG, '书籍已存在')
      }
    }).catch(err => {
      console.log(err)
    })
  },
  delFavorite ({ commit }, favorId) {
    Vue.http.delete(`/book/starbook/${favorId}`).then(res => {
      commit(SET_ERRORMSG, '删除成功')
      store.dispatch('getFavorite')
    }).catch(err => {
      commit(SET_ERRORMSG, err)
    })
  },
  getOrdered ({ commit }) {
    let orderedPending = []
    let orderedSuccess = []
    let orderedCart = {}
    Vue.http.get('/library/order/wait/').then(res => {
      orderedPending = res.data
      Vue.http.get('/library/order/success/').then(res => {
        orderedSuccess = res.data
        orderedCart = {pending: orderedPending, success: orderedSuccess}
        commit('SET_ORDEREDCART', orderedCart)
      })
    }).catch(err => commit(SET_ERRORMSG, err))
  },
  getReadPlan ({ commit }) {
    Vue.http.get('/book/readplan/').then(res => {
      commit(SET_READPLAN, res.data)
    }).catch(err => commit(SET_ERRORMSG, err))
  },
  addReadPlan ({ commit }, form) {
    Vue.http.post('/book/readplan/', form).then(res => {
      store.dispatch('getFavorite')
      commit(SET_ERRORMSG, '添加成功')
    }).catch(err => commit(SET_ERRORMSG, err))
  }
}
