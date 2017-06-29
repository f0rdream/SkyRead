import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Image } from 'react-native'
import { isLoginURL} from '../../Config/APIs'
import CookieManager from 'react-native-cookies'

export default class Home extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      isLogin: -1
    }
    this.getIsLogin = this.getIsLogin.bind(this)
  }

  componentDidMount () {
    this.getIsLogin()
    CookieManager.get('http://example.com', (err, res) => {
      console.log('Got cookies for url', res);
      // Outputs 'user_session=abcdefg; path=/;'
    })
  }

  async getIsLogin () {
    const { navigate } = this.props.navigation
    try {
      let response = await fetch(isLoginURL, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
      let res  = await response.text()
      if (response.status >= 200 && response.status < 400) {
        this.setState({ isLogin: 1 })
        navigate('HomeScreen')
      } else {
        this.setState({ isLogin: 0 })
        navigate('LoginScreen')
      }
    } catch(error) {
      console.log("error: " + error)
    }
  }

  render () {
    return (
      <View style={styles.container}>
        <View style={styles.logoContainer}>
          <Image
            style={styles.logo}
            source={{uri: 'http://cn.vuejs.org/images/logo.png'}}
          />
          <Text>Launch Screen</Text>
        </View>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#3498db'
  },
  logoContainer: {
    alignItems: 'center',
    flexGrow: 1,
    justifyContent: 'center'
  },
  logo: {
    width: 100,
    height: 100
  },
  formContainer: {

  }
})
