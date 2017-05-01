import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/HelloFromVux'

import person from '../pages/person'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/person',
      name: 'person',
      component: person
    }
  ]
})
