import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Image } from 'react-native'
import { Container, Toast } from 'native-base'
import QRScaner from './QRScaner'
import { borrowInfo, returnInfo, orderInfo } from '../../Config/APIs'

export default class Scan extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      booksData: {}
    }
  }

  cancelButton = () => {
    this.props.navigation.goBack()
  }

  getQR = (data) => {
    let qrResult = this.convertData(data)
    qrResult.id = qrResult.id.split('b').splice(0,1)
    getBookInfo(qrResult)
  }

  async getBookInfo (qrObj) {
    let type = qrObj.qrtype
    let form = qrObj
    delete form.pay_id
    let url
    switch (type) {
      case 'borrow':
        url = borrowInfo
        break
      case 'return':
        url = returnInfo
        break
      case 'order':
        url = orderInfo
        break
      default:
        console.log('get Type err')
        return
    }
    try {
      let response = await fetch(url, {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        credentials: 'include',
        body: JSON.stringify(form)
      })
      let res  = await response.text()
      if (response.status >= 200 && response.status < 400) {
        this.props.navigation.navigate('BookScreen', { booksData: res, type: type})
      } else {
        Toast.show({
          supportedOrientations: ['portrait','landscape'],
          text: res.msg,
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
    }
  }

  convertData = (string) => {
    let params = {}, queries, temp, i, l
    // Split into key/value pairs
    queries = queryString.split("&")
    // Convert the array of strings into an object
    for ( i = 0, l = queries.length; i < l; i++ ) {
      temp = queries[i].split('=')
      params[temp[0]] = temp[1]
    }
    return params
  }

  render () {
    return (
      <Container>
        <QRScaner
          onQRRead={data => this.getQR(data)}
          onPressCancel={() => this.cancelButton()}
          cancelButtonVisible={true}
        />
      </Container>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#000'
  },
  // preview: {
  //   flex: 1,
  //   justifyContent: 'flex-end',
  //   alignItems: 'center'
  // },
  // capture: {
  //   flex: 0,
  //   backgroundColor: '#fff',
  //   borderRadius: 5,
  //   padding: 10,
  //   margin: 40
  // }
})