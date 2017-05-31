import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/HelloFromVux'

import person from '../pages/person/person'
import home from '../pages/home/home'
import bookdetail from '../pages/home/children/bookdetail'
import indexpage from '../pages/home/children/indexpage'
import category from '../pages/home/children/category'

import SearchPart from '../components/SearchPart'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '*',
      component: Hello
    },
    {
      path: '/home',
      component: home,
      children: [
        {
          path: 'bookdetail/:isbn13',
          component: bookdetail
        },
        {
          path: 'indexpage',
          component: indexpage
        },
        {
          path: 'category/:typeid',
          component: category
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
