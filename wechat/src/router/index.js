import Vue from 'vue'
import Router from 'vue-router'

import person from '../pages/person/person'
import phonepage from '../pages/person/children/phone'
import notfound from '../pages/404/404'
import related from '../pages/person/children/related'
import nearby from '../pages/person/children/nearby'
import relatedlist from '../pages/person/children/relatedlist'
import bmap from '../pages/person/children/map'
import feedback from '../pages/person/children/feedback'

import home from '../pages/home/home'
import bookdetail from '../pages/home/children/bookdetail'
import indexpage from '../pages/home/children/indexpage'
import category from '../pages/home/children/category'
import list from '../pages/home/children/list'
import comment from '../pages/home/children/comment'
import price from '../pages/home/children/price'

import bookshelf from '../pages/cart/bookshelf'
import renting from '../pages/cart/children/renting'
import scaned from '../pages/cart/children/scaned'
import paying from '../pages/cart/children/paying'
import backing from '../pages/cart/children/backing'
import favorite from '../pages/cart/children/favorite'
import readplan from '../pages/cart/children/readplan'
import addplan from '../pages/cart/children/addplan'
import ordered from '../pages/cart/children/ordered'
import ordertime from '../pages/cart/children/ordertime'
import ordering from '../pages/cart/children/ordering'

import SearchPage from '../pages/search/searchpage'
import SearchResult from '../pages/search/searchresult'

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
        },
        {
          path: 'list/:kind/:itemId',
          component: list
        },
        {
          path: 'comment/:isbn13',
          component: comment
        },
        {
          path: 'price/:isbn13',
          component: price
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
          path: 'renting',
          component: renting
        },
        {
          path: 'paying',
          component: paying
        },
        {
          path: 'backing',
          component: backing
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
        },
        {
          path: 'ordertime/:bookId/:isbn13',
          component: ordertime
        },
        {
          path: 'ordering',
          component: ordering
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
      path: '/person/nearby',
      component: nearby
    },
    {
      path: '/person/related',
      component: related
    },
    {
      path: '/person/related/:index/:item',
      component: relatedlist
    },
    {
      path: '/person/map',
      component: bmap
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
      path: '/addplan',
      component: addplan
    },
    {
      path: '/feedback',
      component: feedback
    }
  ]
})
