import Vue from 'vue'
import 'es6-promise/auto'
import { AjaxPlugin } from 'vux'

const baseURL = '//127.0.0.1:8080'
Vue.use(AjaxPlugin)
Vue.http.defaults.baseURL = baseURL
