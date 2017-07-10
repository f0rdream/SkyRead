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
  },
  LoginScreen: {
    screen: Login,
  },
  ScanScreen: {
    screen: Scan,
  },
  BookScreen: {
    screen: BookInfo,
  }
}, {
  // Default config for all screens
  headerMode: 'none',
  initialRouteName: 'LaunchScreen',
})

// export default () =>
//   (<Root>
//     <PrimaryNav />
//   </Root>)

export default PrimaryNav
