import Vue from 'vue'
import 'es6-promise/auto'
import { AjaxPlugin } from 'vux'

const baseURL = '//115.159.185.170'
Vue.use(AjaxPlugin)
Vue.http.defaults.baseURL = baseURL
Vue.http.defaults.withCredentials = true
