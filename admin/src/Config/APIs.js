

import axios from 'axios'

const baseURL = 'http://skyread.fordream001.cn/'

export const loginURL = baseURL + 'web/android_login/'
export const isLoginURL = baseURL + 'web/is_login/'
export const timesURL = baseURL + 'web/record/sum/'
export const signURL = baseURL + 'web/sign/'
export const signTimesURL = baseURL + 'web/a_info/'
export const borrowInfo = baseURL + 'library/borrow/verify/'
export const orderInfo = baseURL + '/library/order/finish/'
export const returnInfo = baseURL + '/library/return/verify/'
export const borrowConfirm = baseURL + '/library/confirm/' // + something
export const borrowPay = baseURL + '/library/pay_info/'  //+pay_id
export const adminInfoURL = baseURL + '/web/info/'

const xsrfCookieName = 'csrftoken' // default
const xsrfHeaderName = 'X-CSRFToken' // default
const withCredentials = true
axios.default.withCredentials = true
axios.xsrfCookieName = 'csrftoken'
axios.xsrfHeaderName = 'X-CSRFToken'
// customConfig = { xsrfHeaderName, xsrfCookieName, withCredentials}
// axios.default = {...axios.default, ...customConfig}

export { axios }



// // our "constructor"
// const instance = (baseURL = 'https://api.github.com/') => {
//   // ------
//   // STEP 1
//   // ------
//   //
//   // Create and configure an apisauce-based api object.
//   //
//   const api = apisauce.create({
//     // base URL is read from the "constructor"
//     baseURL,
//     // here are some default headers
//     headers: {
//
//     },
//     // 10 second timeout...
//     timeout: 10000
//   })
//
//   // ------
//   // STEP 2
//   // ------
//   //
//   // Define some functions that call the api.  The goal is to provide
//   // a thin wrapper of the api layer providing nicer feeling functions
//   // rather than "get", "post" and friends.
//   //
//   // I generally don't like wrapping the output at this level because
//   // sometimes specific actions need to be take on `403` or `401`, etc.
//   //
//   // Since we can't hide from that, we embrace it by getting out of the
//   // way at this level.
//   //
//   const getRoot = () => api.get('')
//   const getRate = () => api.get('rate_limit')
//   const getUser = (username) => api.get('search/users', {q: username})
//
//   // ------
//   // STEP 3
//   // ------
//   //
//   // Return back a collection of functions that we would consider our
//   // interface.  Most of the time it'll be just the list of all the
//   // methods in step 2.
//   //
//   // Notice we're not returning back the `api` created in step 1?  That's
//   // because it is scoped privately.  This is one way to create truly
//   // private scoped goodies in JavaScript.
//   //
//   return {
//     // a list of the API functions from step 2
//     getRoot,
//     getRate,
//     getUser
//   }
// }
//
// // let's return back our create method as the default.
// export default {
//   create
// }
//
//
// // import axios from 'axios'
//
//
// const baseURL = 'http://skyread.fordream001.cn/'
//
// async get (url, callback) {
//   try {
//     let response = await fetch(timesURL, {
//       headers: {
//         'Accept': 'application/json',
//         'Content-Type': 'application/json'
//       }
//     })
//     let res  = await response.text()
//     if (response.status >= 200 && response.status < 400) {
//       callback(res)
//     } else {
//       console.log(res)
//     }
//   } catch(error) {
//     console.log("error: " + error)
//   }
// }
//
