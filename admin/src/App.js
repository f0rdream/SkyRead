import React from 'react'
import {
  AppRegistry,
  Text,
  View,
  Button,
  Dimensions,
  StyleSheet,
  TouchableHighlight,
  Image,
} from 'react-native';
import { StackNavigator, TabNavigator } from 'react-navigation'
import { Colors } from './Themes/'
import Navigation from './Navigation/AppNavigation'
import Reactotron from 'reactotron-react-native'

class AppContainer extends React.Component {
  // constructor (props) {
  //   super(props)
  //   this.state = {
  //     isLogin: -1
  //   }
  //   this.getIsLogin = this.getIsLogin.bind(this)
  // }
  // componentWillReceiveProps () {
  //   this.getIsLogin()
  // }
  // componentDidMount () {
  //   this.getIsLogin()
  // }
  //
  // async getIsLogin () {
  //   // const { navigate } = this.props.navigation
  //   try {
  //     let response = await fetch(isLoginUrl, {
  //       headers: {
  //         'Accept': 'application/json',
  //         'Content-Type': 'application/json'
  //       }
  //     })
  //     let res  = await response.text()
  //     if (response.status >= 200 && response.status < 400) {
  //       console.log('before set state')
  //       this.setState({ isLogin: 1 }, () => {
  //         console.log('set done')
  //       })
  //       console.log('after set state')
  //       // navigate('HomeScreen')
  //       console.log('res ' + res)
  //     } else {
  //       this.setState({ isLogin: 0 }, () => {
  //         console.log('set done')
  //       })
  //       // navigate('LoginScreen')
  //       console.log('Login err: ' + error)
  //     }
  //   } catch(error) {
  //     console.log("error: " + error)
  //   }
  // }

  render () {
    return (
      <View style={{flex: 1}}>
        <Navigation/>
      </View>
    )
  }
}

export default AppContainer

// const PrimaryNav = StackNavigator({
//   LaunchScreen: { screen: Login },
//   LoginScreen: {
//     screen: Login,
//     navigationOptions: { title: 'Login' }
//   }
// }, {
//   // Default config for all screens
//   headerMode: 'none',
//   initialRouteName: 'LaunchScreen',
//   // navigationOptions: {
//   //   headerStyle: styles.header
//   // }
// })
//
// // const styles = StyleSheet.create({
// //   header: {
// //     backgroundColor: Colors.background
// //   }
// // })
//
// export default PrimaryNav
