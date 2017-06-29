import { timePY2JS } from '@/config/utils'

export default {
  readPlanGetter (state) {
    if (!state.readPlan) {
      return state.readPlan
    }
    let formated = state.readPlan.map(item => {
      return {...item, ...{begin_time: timePY2JS(item.begin_time), end_time: timePY2JS(item.end_time)}}
    })
    return formated
  },
  favoriteList (state) {
    return state.favorite.map(item => {
      return { name: item.short_info.title, value: item.short_info.isbn13 }
    })
  }
}
