import Vue from 'vue'
import 'es6-promise/auto'
import { AjaxPlugin } from 'vux'

const baseURL = ''
Vue.use(AjaxPlugin)
Vue.http.defaults.baseURL = baseURL
Vue.http.defaults.withCredentials = true
Vue.http.defaults.xsrfCookieName = 'csrftoken'
Vue.http.defaults.xsrfHeaderName = 'X-CSRFToken'
