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
import Login from './src/components'

const PrimaryNav = StackNavigator({
  LaunchScreen: { screen: LoginScreen },
  LoginScreen: {
    screen: LoginScreen,
    navigationOptions: { title: 'Login' }
  }
}, {
  // Default config for all screens
  headerMode: 'none',
  initialRouteName: 'LaunchScreen',
  navigationOptions: {
    headerStyle: styles.header
  }
})

export default PrimaryNav
