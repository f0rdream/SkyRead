import Vue from 'vue'
import store from './index'
import { SET_ACCOUNTSINFO, SET_ERRORMSG, SET_QRINFO, SET_SCANEDCART, SET_RENTINGCART, SET_FAVROITES, SET_READPLAN, SET_HAVEPHONE, SET_CURRENTTAB } from './mutation-types'
import '../config/ajax'
import Router from '../router/index'

export default {
  setErrMsg ({ commit }, obj) {
    commit(SET_ERRORMSG, obj)
  },
  getAccountsInfo ({ commit }, info) {
    Vue.http.get('/accounts/').then((res) => {
      commit(SET_ACCOUNTSINFO, res.data)
      commit(SET_HAVEPHONE, res.data.have_phone)
    })
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
      console.log(err.response.data)
    })
  },
  delScanedList ({commit}, itemId) {
    Vue.http.delete(`/library/borrow/${itemId}`).then(res => {
      commit(SET_ERRORMSG, {text: '删除成功'})
      store.dispatch('getScanedList')
    }).catch(err => {
      store.dispatch('getScanedList')
      commit(SET_ERRORMSG, {text: '删除失败', type: 'cancel'})
      console.log(err.response.data)
    })
  },
  getRentingList ({ commit }) {
    Vue.http.get('/library/return/').then(res => {
      commit(SET_RENTINGCART, res.data)
    }).catch(err => {
      console.log(err.response.data)
    })
  },
  getRentingQR ({ commit, state }, indexList) {
    // let idList
    // for (let index of indexList) {
    //   idList.push(state.rentingCart[index].id)
    // }
    Vue.http.post('/library/return/qrcode/', {id_list: indexList}).then(res => {
      commit(SET_QRINFO, res.data)
      Router.push('/bookshelf/backing')
    })
  },
  reNewRenting ({ commit }, id) {
    Vue.http.post('/library/return/continue/', {id: id}).then(res => {
      store.dispatch('getRentingList')
      commit(SET_ERRORMSG, {text: '续借成功'})
    }).catch(err => commit(SET_ERRORMSG, {text: err.response.data, type: 'cancel'}))
  },

  getFavorite ({ commit }) {
    Vue.http.get('/book/starbook/').then(res => {
      commit(SET_FAVROITES, res.data)
    }).catch(err => {
      console.log(err.response.data)
    })
  },
  addFavorite ({ commit }, isbn13) {
    Vue.http.post('/book/starbook/', { isbn13: isbn13 }).then(res => {
      res = res.data
      if (res.error_code === 0) {
        commit(SET_ERRORMSG, {text: '加入成功'})
      } else if (res.error_code === 98) {
        commit(SET_ERRORMSG, {text: '书籍已存在', type: 'cancel'})
      }
    }).catch(err => {
      console.log(err.response.data)
    })
  },
  delFavorite ({ commit }, favorId) {
    Vue.http.delete(`/book/starbook/${favorId}`).then(res => {
      commit(SET_ERRORMSG, {text: '删除成功'})
      store.dispatch('getFavorite')
    }).catch(err => {
      commit(SET_ERRORMSG, {text: err.response.data, type: 'cancel'})
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
    }).catch(err => commit(SET_ERRORMSG, {text: err.response.data, type: 'cancel'}))
  },
  delOrdered ({ commit }, payload) {
    if (payload.type === 1) {
      Vue.http.delete(`/library/order/wait/${payload.id}`).then(res => {
        commit(SET_ERRORMSG, {text: '删除成功'})
        store.dispatch('getOrdered')
      }).catch(err => {
        commit(SET_ERRORMSG, err.response.data, 'cancel')
      })
    } else {
      Vue.http.delete(`/library/order/success/${payload.id}`).then(res => {
        commit(SET_ERRORMSG, {text: '删除成功'})
        store.dispatch('getOrdered')
      }).catch(err => {
        commit(SET_ERRORMSG, {text: err.response.data, type: 'cancel'})
      })
    }
  },
  getOrderQR ({ commit }, qrinfo) {
    commit(SET_QRINFO, qrinfo)
    Router.push('/bookshelf/ordering')
  },
  orderTime ({ commit }, form) {
    Vue.http.post('/library/order/success/', form).then(res => {
      commit(SET_ERRORMSG, {text: '预约成功'})
    }).catch(err => commit(SET_ERRORMSG, {text: err.response.data, type: 'cancel'}))
  },
  getReadPlan ({ commit }) {
    Vue.http.get('/book/readplan/').then(res => {
      commit(SET_READPLAN, res.data)
    }).catch(err => commit(SET_ERRORMSG, {text: err.response.data, type: 'cancel'}))
  },
  addReadPlan ({ commit }, form) {
    Vue.http.post('/book/readplan/', form).then(res => {
      store.dispatch('getReadPlan')
      commit(SET_ERRORMSG, {text: '添加成功'})
    }).catch(err => commit(SET_ERRORMSG, {text: err.response.data, type: 'cancel'}))
  },
  delReadPlan ({ commit }, id) {
    Vue.http.delete(`/book/readplan/${id}`).then(res => {
      store.dispatch('getReadPlan')
      commit(SET_ERRORMSG, {text: '删除成功'})
    }).catch(err => commit(SET_ERRORMSG, {text: err.response.data, type: 'cancel'}))
  },
  setCurrentTab ({ commit }, tab) {
    commit(SET_CURRENTTAB, tab)
  }
}
