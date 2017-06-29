// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import FastClick from 'fastclick'
import VueRouter from 'vue-router'
import App from './App'
import router from './router'
import store from './store/index'
import './config/ajax'
import { WechatPlugin, ToastPlugin } from 'vux'

Vue.use(VueRouter)
Vue.use(WechatPlugin)
Vue.use(ToastPlugin)

FastClick.attach(document.body)

Vue.config.productionTip = true

/* eslint-disable no-new */
new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app-box')
