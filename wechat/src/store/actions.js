import Vue from 'vue'
import { SET_WECHATSIGN, SET_BORROWQRINFO, SET_SCANEDCART } from './mutation-types'
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
  getBorrowQR ({ commit, state }, bookId) {
    let idList = []
    if (!bookId) {
      for (let book of state.scanedCart) {
        idList.push(book.id)
      }
    } else {
      idList = [bookId]
    }
    Vue.http.post('/library/borrow/qrcode/', {id_list: idList}).then(res => {
      commit(SET_BORROWQRINFO, res.data)
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
  }
}
