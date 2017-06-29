import { StackNavigator } from 'react-navigation'

import Login from '../Components/Login/Login'
import Home from '../Components/Home/Home'
import Launch from '../Components/Launch/Launch'
import Scan from '../Components/Scan/Scan'
import BookInfo from '../Components/BookInfo/BookInfo'

import styles from './Styles/NavigationStyles'

// Manifest of possible screens
const PrimaryNav = StackNavigator({
  LaunchScreen: { screen: Launch },
  HomeScreen: {
    screen: Home,
    navigationOptions: { title: '图书管理员' }
  },
  LoginScreen: {
    screen: Login,
    navigationOptions: { title: 'Login' }
  },
  ScanScreen: {
    screen: Scan,
    navigationOptions: { title: '扫码' }
  },
  BookScreen: {
    screen: BookInfo,
    navigationOptions: { title: '书籍详情' }
  }
}, {
  // Default config for all screens
  // headerMode: 'none',
  initialRouteName: 'LaunchScreen',
  navigationOptions: {
    headerStyle: styles.header
  }
})

export default PrimaryNav
