import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, AsyncStorage } from 'react-native'
import { axios, loginURL } from '../../Config/APIs'
import { Toast } from 'native-base'

export default class LoginForm extends React.Component {
  constructor (props) {
      super (props)

      this.state = {
        username: '',
        password: '',
        error: '',
        showProgress: false,
      }
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
      if (response.status >= 200 && response.status < 300) {
        this.setState({error: ''})
        this.props.navigation.navigate('HomeScreen')
      } else {
        this.setState({error: res})
        Toast.show({
          supportedOrientations: ['portrait','landscape'],
          text: res,
          position: 'bottom',
          buttonText: 'Okay'
        })
      }
    } catch(err) {
      Toast.show({
        supportedOrientations: ['portrait','landscape'],
        text: err,
        position: 'bottom',
        buttonText: 'Okay'
      })
      this.setState({error: err})
      console.log("error: " + err)
    }
  }

  render () {
    return (
      <View style={styles.container}>
        <TextInput
          placeholder="Plase enter the username"
          returnKeyType="next"
          onSubmitEditing={() => this.passwordInput.focus()}
          keybordType="default"
          style={styles.input}
          onChangeText={(text) => this.setState({username: text})}
        />
        <TextInput
          placeholder="Plase enter the password"
          returnKeyType="go"
          secureTextEntry
          ref={(input) => this.passwordInput = input}
          keybordType="default"
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
    color: '#FFF',
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
