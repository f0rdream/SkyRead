import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/HelloFromVux'

import person from '../pages/person/person'

import home from '../pages/home/home'
import bookdetail from '../pages/home/children/bookdetail'
import indexpage from '../pages/home/children/indexpage'
import SearchPart from '../components/SearchPart'

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
        },
        {
          path: 'indexpage',
          component: indexpage
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
    },
    {
      path: '/searchpart',
      component: SearchPart
    }
  ]
})
