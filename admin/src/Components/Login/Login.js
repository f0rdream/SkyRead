import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Image } from 'react-native'
import LoginForm from './LoginForm'
import { Container } from 'native-base'


export default class Login extends React.Component {
  render () {
    return (
      <Container>
        <View style={styles.logoContainer}>
          <Image
            style={styles.logo}
            source={{uri: 'http://cn.vuejs.org/images/logo.png'}}
          />
        </View>
        <View style={styles.formContainer}>
          <LoginForm/>
        </View>
      </Container>
    )
  }
}

const styles = StyleSheet.create({
  container: {
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
