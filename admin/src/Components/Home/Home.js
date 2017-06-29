import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Image } from 'react-native'
import AdminInfo from './AdminInfo'
import { Colors } from '../../Themes/'
import { Button } from 'native-base'

export default class Home extends React.Component {
  constructor(props) {
    super(props)
  }
  handlePressScan = () => {
    this.props.navigation.navigate('ScanScreen')
  }

  render () {
    return (
      <View style={styles.container}>
        <AdminInfo/>
        <View style={styles.btnContainer}>
          <Button info large rounded onPress={this.handlePressScan}>
            <Text style={styles.btnText}>扫码</Text>
          </Button>
        </View>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.background
  },
  btnText: {
    color: Colors.btnText
  },
  btnContainer: {
    flexDirection: 'row',
    justifyContent: 'center'
  }
})
