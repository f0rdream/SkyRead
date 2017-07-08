import Vue from 'vue'
import Router from 'vue-router'

import person from '../pages/person/person'
import phonepage from '../pages/person/children/phone'
import notfound from '../pages/404/404'

import home from '../pages/home/home'
import bookdetail from '../pages/home/children/bookdetail'
import indexpage from '../pages/home/children/indexpage'
import category from '../pages/home/children/category'

import bookshelf from '../pages/cart/bookshelf'
import lending from '../pages/cart/children/lending'
import scaned from '../pages/cart/children/scaned'
import paying from '../pages/cart/children/paying'
import favorite from '../pages/cart/children/favorite'
import readplan from '../pages/cart/children/readplan'
import addplan from '../pages/cart/children/addplan'
import ordered from '../pages/cart/children/ordered'

import SearchPage from '../pages/search/searchpage'
import SearchResult from '../pages/search/searchresult'
import RelatedPerson from '../pages/home/children/relatedperson.vue'

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
        },
        {
          path: 'paying',
          component: paying
        },
        {
          path: 'favorite',
          component: favorite
        },
        {
          path: 'readplan',
          component: readplan
        },
        {
          path: 'ordered',
          component: ordered
        }
      ]
    },
    {
      path: '/person',
      component: person
    },
    {
      path: '/person/phone',
      component: phonepage
    },
    {
      path: '/bookdetail',
      component: bookdetail
    },
    {
      path: '/search',
      component: SearchPage
    },
    {
      path: '/search/:keyword',
      component: SearchResult
    },
    {
      path: '/relatedperson/:personIndex/:personName',
      component: RelatedPerson
    },
    {
      path: '/addplan',
      component: addplan
    }
  ]
})
