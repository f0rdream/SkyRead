import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, AsyncStorage } from 'react-native'
import { axios, loginURL, isLoginURL } from '../../Config/APIs'
import { Toast } from 'native-base'
import { NavigationActions } from 'react-navigation'

export default class LoginForm extends React.Component {
  constructor (props) {
      super (props)

      this.state = {
        username: '',
        password: '',
        error: '',
        showProgress: false,
      }
      this.getIsLogin = this.getIsLogin.bind(this)
  }

  _navigateTo = (routeName: string) => {
    const actionToDispatch = NavigationActions.reset({
      index: 0,
      actions: [NavigationActions.navigate({ routeName })]
    })
    this.props.navigation.dispatch(actionToDispatch)
  }

  async onLoginPressed() {
    // try {
    //   let res = await axios.post(loginURL, {
    //     username: this.state.username,
    //     password: this.state.password
    //   })
    // } catch (err) {
    //   Toast.show({
    //     supportedOrientations: ['portrait','landscape'],
    //     text: err,
    //     position: 'bottom',
    //     buttonText: 'Okay'
    //   })
    // }
    try {
      let response = await fetch(loginURL, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify({
          username: this.state.username,
          password: this.state.password
        })
      })
      let res  = await response.text()
      if (response.status >= 200 && response.status < 400) {
        this._navigateTo('HomeScreen')
        Toast.show({
          supportedOrientations: ['portrait','landscape'],
          text: res,
          position: 'bottom',
          buttonText: 'Okay'
        })
      } else {
        this.getIsLogin()
        Toast.show({
          supportedOrientations: ['portrait','landscape'],
          text: res,
          position: 'bottom',
          buttonText: 'Okay'
        })
      }
    } catch(err) {
      this.getIsLogin()
      Toast.show({
        supportedOrientations: ['portrait','landscape'],
        text: err,
        position: 'bottom',
        buttonText: 'Okay'
      })
    }
  }

  async getIsLogin () {
    try {
      let response = await fetch(isLoginURL, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
      let res  = await response.text()
      if (response.status >= 200 && response.status < 400) {
        this._navigateTo('HomeScreen')
      }
    } catch(error) {
      console.log("error: " + error)
    }
  }

  render () {
    return (
      <View style={styles.container}>
        <TextInput
          placeholder="用户名"
          returnKeyType="next"
          onSubmitEditing={() => this.passwordInput.focus()}
          style={styles.input}
          onChangeText={(text) => this.setState({username: text})}
        />
        <TextInput
          placeholder="密码"
          returnKeyType="go"
          secureTextEntry
          ref={(input) => this.passwordInput = input}
          style={styles.input}
          onChangeText={(text) => this.setState({password: text})}
        />
        <TouchableOpacity
          onPress={this.onLoginPressed.bind(this)}
          style={styles.buttonContainer}
          >
          <Text style={styles.buttonText}>LOGIN</Text>
        </TouchableOpacity>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    padding: 20
  },
  input: {
    height: 40,
    backgroundColor: 'rgba(255,255,255, 0.2)',
    marginBottom: 20,
    color: '#333',
    paddingHorizontal: 10
  },
  buttonContainer: {
    backgroundColor: '#2980b9',
    paddingVertical: 15
  },
  buttonText: {
    textAlign: 'center',
    color: '#FFF'
  }
})
