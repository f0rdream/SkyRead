import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Image } from 'react-native'
import { Colors } from '../../Themes/'
import { Button, Container } from 'native-base'
import { adminInfoURL } from '../../Config/APIs'

export default class AdminInfo extends React.Component {
  constructor (props) {
    super(props)
    this.state = {
      signDay: '0',
      returnTime: '0',
      borrowTime: '0',
      orderTime: '0',
      signStat: false
    }
    this.getInfo = this.getInfo.bind(this)
    this.attend = this.attend.bind(this)
  }

  componentDidMount () {
    this.getInfo()
  }

  async getInfo () {
    try {
      let response = await fetch(adminInfoURL, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
      let res  = await response.text()
      if (response.status >= 200 && response.status < 400) {
        this.setState({
          returnTime: res.return,
          borrowTime: res.borrow,
          orderTime: res.order,
          signDay: res.times
        })
      } else {
        console.log(res)
      }
    } catch(error) {
      console.log("error: " + error)
    }
  }

  async attend () {
    try {
      let response = await fetch(signUrl, {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      })
      let res  = await response.text()
      if (response.status >= 200 && response.status < 400) {
        this.setState({
          signStat: true
        })
      } else {
        console.log(res)
      }
    } catch(error) {
      console.log("error: " + error)
    }
  }

  render () {
    let signBtn
    if (this.state.signStat) {
      signBtn = (
        <Button style={styles.logo} info rounded small onPress={this.attend}>
          <Text style={styles.btnText}>签到</Text>
        </Button>
      )
    } else {
      signBtn = (
        <Button style={styles.logo} info rounded small disabled>
          <Text style={styles.btnText}>已签到</Text>
        </Button>
      )
    }

    return (
      <View style={styles.cardContainer} elevation={3}>
        <View style={styles.logoContainer}>
          <Image
            style={styles.logo}
            source={{uri: 'http://cn.vuejs.org/images/logo.png'}}
          />
          <View style={styles.btnContainer}>
            {signBtn}
          </View>
        </View>
        <View style={styles.infoPart}>
          <View style={[styles.infoRow, styles.infoRowTop]}>
            <View style={[styles.infoContainer, styles.infoContainerLeft]}>
              <Text>已打卡</Text>
              <Text><Text>{this.state.signDay}</Text> 天</Text>
            </View>
            <View style={styles.infoContainer}>
              <Text>处理订阅</Text>
              <Text><Text>{this.state.orderTime}</Text> 天</Text>
            </View>
          </View>
          <View style={styles.infoRow}>
            <View style={[styles.infoContainer, styles.infoContainerLeft]}>
              <Text>处理借书</Text>
              <Text><Text>{this.state.borrowTime}</Text> 天</Text>
            </View>
            <View style={styles.infoContainer}>
              <Text>处理还书</Text>
              <Text><Text>{this.state.returnTime}</Text> 天</Text>
            </View>
          </View>
        </View>
      </View>
    )
  }
}

const styles = StyleSheet.create({
  cardContainer: {
    marginHorizontal: 25,
    marginVertical: 40,
    backgroundColor: '#ffffff',
    borderRadius: 8,
    paddingVertical: 15,
  },
  logoContainer: {
    alignItems: 'center',
    justifyContent: 'center'
  },
  logo: {
    width: 80,
    height: 80
  },
  infoPart: {
    margin: 10
  },
  infoRow: {
    flexDirection: 'row',
  },
  infoRowTop: {
    borderBottomWidth: 2,
    borderColor: '#ddd'
  },
  infoContainer: {
    flex: 1,
    alignItems: 'center',
    marginVertical: 15
  },
  infoContainerLeft: {
    borderRightWidth: 2,
    borderColor: '#ddd'
  },
  btnText: {
    color: Colors.btnText
  }
})
