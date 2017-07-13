import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Image } from 'react-native'
import { Container, Toast } from 'native-base'
import QRScaner from './QRScaner'
import { borrowInfo, returnInfo, orderInfo } from '../../Config/APIs'

export default class Scan extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      booksData: {},
      stop: false
    }
  }

  cancelButton = () => {
    this.props.navigation.goBack()
  }

  getQR = (data) => {
    try {
      let qrResult = this.convertData(data.data)
      if (qrResult.id) {
        qrResult.id_list = qrResult.id.split('b')
        qrResult.id_list.splice(0,1)
        delete qrResult.id
      }
      if (!this.state.stop) {
        this.getBookInfo(qrResult)
      }
    } catch (err) {
      console.log(err)
    }
  }

  async getBookInfo (qrObj) {
    let type = qrObj.qrtype
    let form = qrObj
    let url
    switch (type) {
      case 'borrow':
        url = borrowInfo
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
          console.log(JSON.stringify(form))
          let res  = await response.json()
          console.log(res);
          if (response.status >= 200 && response.status < 400) {
            this.setState({stop: true})
            this.props.navigation.navigate('BookScreen', { booksData: res, type: type, pay_id: qrObj.pay_id})
          } else {
            console.log('Toast before')
            Toast.show({
              supportedOrientations: ['portrait','landscape'],
              text: '扫描失败',
              position: 'bottom',
              buttonText: 'Okay'
            })
          }
        } catch(err) {
          Toast.show({
            supportedOrientations: ['portrait','landscape'],
            text: '扫描失败',
            position: 'bottom',
            buttonText: 'Okay'
          })
        }
        break
      case 'return':
        url = returnInfo
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
          console.log(JSON.stringify(form))
          console.log(response);
          let res  = await response.json()
          console.log(res);
          if (response.status >= 200 && response.status < 400) {
            this.setState({stop: true})
            this.props.navigation.navigate('BookScreen', { booksData: res, type: type, return_id: qrObj.return_id, id_list: qrObj.id_list})
          } else {
            console.log('Toast before')
            Toast.show({
              supportedOrientations: ['portrait','landscape'],
              text: '扫描失败',
              position: 'bottom',
              buttonText: 'Okay'
            })
          }
        } catch(err) {
          Toast.show({
            supportedOrientations: ['portrait','landscape'],
            text: '扫描失败',
            position: 'bottom',
            buttonText: 'Okay'
          })
        }
        break
      case 'order':
        url = orderInfo
        this.setState({stop: true})
        this.props.navigation.navigate('BookScreen', { booksData: form, type: type})
        break
      default:
        console.log('get Type err')
        return
    }
  }

  convertData = (queryString) => {
    let params = {}, queries, temp, i, l
    // Split into key/value pairs
    queryString = queryString.split('?')[1]
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
