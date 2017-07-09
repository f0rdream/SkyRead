import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Image } from 'react-native'
import { Button, Card } from 'native-base'
import { borrowInfo, returnInfo, orderInfo } from '../../Config/APIs'


export default class BookInfo extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      pageType: this.props.type,
      // books: this.props.booksData.books,
      // order: this.props.booksData.order
    }
  }

  // getTypeInfo = () => {
  //   let type = this.props.qrResult.qrtype
  //   this.setState({pageType: type})
  // }
  //
  // async getBookInfo (type) {
  //   let url
  //   switch (type) {
  //     case 'borrow':
  //       url = borrowInfo
  //       break
  //     case 'return':
  //       url = returnInfo
  //       break
  //     case 'order':
  //       url = orderInfo
  //       break
  //     default:
  //       console.log('get Type err')
  //       return
  //   }
  //   try {
  //     let response = await fetch(url, {
  //       headers: {
  //         'Accept': 'application/json',
  //         'Content-Type': 'application/json'
  //       }
  //     })
  //     let res  = await response.text()
  //     if (response.status >= 200 && response.status < 400) {
  //       this.setState({
  //         booksData: res
  //       })
  //     } else {
  //       console.log(res)
  //     }
  //   } catch(error) {
  //     console.log("error: " + error)
  //   }
  // }


  render () {
    let list = [1, 1]
    let booksDom = []
    for (let i in list) {
      booksDom.push(<InfoPart/>)
    }
    return (
      <View style={styles.container}>
        <View style={styles.cardContainer} elevation={3}>
          <View style={styles.titlePart}>
            <Text style={styles.titleText}>账单明细</Text>
          </View>
          <View style={styles.infoPart}>
            {booksDom}
          </View>
          <View style={styles.payPart}>
            <PayPart/>
          </View>
          <View style={styles.confirmPart}>
            <ConfirmBtn/>
          </View>
        </View>
      </View>
    )
  }
}

class InfoPart extends React.Component {
  render () {
    return (
      <View style={styles.infoContainer}>
        <View style={styles.logoContainer}>
          <Image
            style={styles.logo}
            source={{uri: 'https://img3.doubanio.com/lpic/s1074793.jpg'}}
          />
        </View>
        <View style={styles.rightPart}>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>书名</Text>
            <Text style={styles.rightRight}>编译原理</Text>
          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>ISBN</Text>
            <Text style={styles.rightRight}>432423432</Text>
          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>借出时间</Text>
            <Text style={styles.rightRight}>书名</Text>
          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>归还时间</Text>
            <Text style={styles.rightRight}>书名</Text>
          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>借书人</Text>
            <Text style={styles.rightRight}>书名</Text>
          </View>
        </View>
      </View>
    )
  }
}

class PayPart extends React.Component {
  render () {
    return (
      <View style={styles.payContainer}>
        <View style={styles.payRow}>
          <Text style={styles.payLeft}>交易订单号</Text>
          <Text style={styles.payRight}>12345</Text>
        </View>
        <View style={styles.payRow}>
          <Text style={styles.payLeft}>支付时间</Text>
          <Text style={styles.payRight}>2016-5-22</Text>
        </View>
      </View>
    )
  }
}

class ConfirmBtn extends React.Component {
  render () {
    return (
      <View style={styles.confirmContainer}>
        <Button info rounded>
          <Text style={styles.confirmText}>确认信息</Text>
        </Button>
        {/* <TouchableOpacity style={styles.confirmBtn}>
          <Text style={styles.confirmText}>确定</Text>
        </TouchableOpacity> */}
      </View>
    )
  }
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#f7f7f7',
    flex: 1
  },
  cardContainer: {
    marginHorizontal: 25,
    marginTop: 25,
    backgroundColor: '#ffffff',
    borderRadius: 8,
    paddingVertical: 15,
    // shadowOffset: '5, 5'
  },
  titlePart: {
    alignItems: 'center',
    flex: 0
  },
  titleText: {
    fontSize: 18,
    fontWeight: '700'
  },
  infoPart: {
    marginTop: 10
  },
  infoContainer: {
    flexDirection: 'row',
    marginHorizontal: 15,
    paddingVertical: 10,
    borderBottomWidth: 2,
    borderColor: '#ccc'
  },
  logoContainer: {
    justifyContent: 'center',
    marginLeft: 5,
    marginRight: 10
  },
  logo: {
    width: 100,
    height: 142
  },
  rightPart: {
    justifyContent: 'center',
    flex: 1
  },
  rightRow: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
  },
  rightLeft: {
    flexDirection: 'row',
    flex: 1,
    fontSize: 14
  },
  rightRight: {
    flexDirection: 'row',
    flex: 1,
    fontSize: 14
  },
  payPart: {
    marginTop: 10
  },
  payContainer: {
    marginHorizontal: 15,
    paddingBottom: 10,
    borderBottomWidth: 2,
    borderColor: '#ccc'
  },
  payRow: {
    flexDirection: 'row',
    justifyContent: 'flex-start',
    marginHorizontal: 5
  },
  payLeft: {
    flexBasis: 100
  },
  confirmPart: {
    marginTop: 10
  },
  confirmContainer: {
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: 10
  },
  confirmText: {
    color: '#eee'
  }
})
