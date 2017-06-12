import Vue from 'vue'
import Router from 'vue-router'

import person from '../pages/person/person'
import notfound from '../pages/404/404'

import home from '../pages/home/home'
import bookdetail from '../pages/home/children/bookdetail'
import indexpage from '../pages/home/children/indexpage'
import category from '../pages/home/children/category'

import bookshelf from '../pages/cart/bookshelf'
import lending from '../pages/cart/children/lending'
import scaned from '../pages/cart/children/scaned'

import SearchPart from '../components/SearchPart'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '*',
      component: notfound
    },
    {
      path: '/',
      redirect: '/home/indexpage'
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
      path: '/bookshelf',
      component: bookshelf,
      children: [
        {
          path: 'scaned',
          component: scaned
        },
        {
          path: 'lending',
          component: lending
        }
      ]
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
