import Vue from 'vue'
import 'es6-promise/auto'
import { AjaxPlugin } from 'vux'

const baseURL = '//123.207.110.178'
Vue.use(AjaxPlugin)
Vue.http.defaults.baseURL = baseURL
