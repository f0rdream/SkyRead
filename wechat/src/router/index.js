import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/HelloFromVux'

import person from '../pages/person/person'

import home from '../pages/home/home'
import bookdetail from '../pages/home/children/bookdetail'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/home',
      component: home,
      children: [
        {
          path: 'bookdetail',
          component: bookdetail
        }
      ]
    },
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/person',
      component: person
    },
    {
      path: '/bookdetail',
      component: bookdetail
    }
  ]
})
