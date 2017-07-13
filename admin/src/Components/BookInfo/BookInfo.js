import React from 'react'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Image } from 'react-native'
import { Button, Card, Toast, Container } from 'native-base'
import { borrowInfo, returnInfo, orderInfo, confirmBorrow, confirmOrder, confirmReturn } from '../../Config/APIs'


export default class BookInfo extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      pageType: this.props.navigation.state.params.type,
      books: this.props.navigation.state.params.booksData,
      toast: {
        show: false,
        word: ''
      }
    }
  }

  setToast = (obj) => {
    this.setState(toast, obj)
  }

  // getTypeInfo = () => {
  //   let type = this.props.qrResult.qrtype
  //   this.setState({pageType: type})
  // }

  // async function getBookInfo (type) {
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

    if (this.state.pageType === 'borrow') {
      let booksDom = []
      for (let i in this.state.books.bookinfo) {
        booksDom.push(<InfoPart book={this.state.books.bookinfo[i]} key={this.state.books.bookinfo[i].id}/>)
      }
      return (
        <Container>
          <View style={styles.cardContainer} elevation={3}>
            <View style={styles.titlePart}>
              <Text style={styles.titleText}>书籍明细</Text>
            </View>
            <View style={styles.infoPart}>
              {booksDom}
            </View>
            <View style={styles.payPart}>
              <PayPart price={this.state.books.price}/>
            </View>
            <View style={styles.confirmPart}>
              <ConfirmBtn type={this.state.pageType} pay_id={this.props.navigation.state.params.pay_id}/>
            </View>
            <View>
              <Toast
                showToast={this.state.toast.show}
                buttonText="Okay"
                buttonPress={()=> this.setState({
                  showToast: !this.state.showToast
                })}
                position="bottom">
                <Text>{this.state.toast.word}</Text>
              </Toast>
            </View>
          </View>
        </Container>
      )
    } else if (this.state.pageType === 'order') {
      return (
        <Container>
          <View style={styles.cardContainer} elevation={3}>
            <View style={styles.titlePart}>
              <Text style={styles.titleText}>预定书籍</Text>
            </View>
            <View style={styles.infoPart}>
              <InfoPartOrder book={this.state.books}/>
            </View>
            <View style={styles.confirmPart}>
              <ConfirmBtn type={this.state.pageType} order_id={this.state.books.order_id}/>
            </View>
          </View>
        </Container>
      )
    } else if (this.state.pageType === 'return') {
      let booksDom = []
      for (let i in this.state.books) {
        booksDom.push(<InfoPart book={this.state.books[i]} key={this.state.books[i].id}/>)
      }
      console.log('BOok dom' + booksDom)
      return (
        <Container>
          <View style={styles.cardContainer} elevation={3}>
            <View style={styles.titlePart}>
              <Text style={styles.titleText}>书籍明细</Text>
            </View>
            <View style={styles.infoPart}>
              {booksDom}
            </View>
            <View style={styles.confirmPart}>
              <ConfirmBtn type={this.state.pageType} id_list={this.props.navigation.state.params.id_list} return_id={this.props.navigation.state.params.return_id}/>
            </View>
          </View>
        </Container>
      )
    } else {
      return (<View></View>)
    }
  }
}

class InfoPart extends React.Component {
  constructor (props) {
    super(props)
  }

  render () {
    let book = this.props.book
    return (
      <View style={styles.infoContainer}>
        <View style={styles.logoContainer}>
          <Image
            style={styles.logo}
            source={{uri: book.image}}
          />
        </View>
        <View style={styles.rightPart}>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>书名</Text>
            <Text style={styles.rightRight}>{book.title}</Text>
          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>ISBN</Text>
            <Text style={styles.rightRight}>{book.isbn13}</Text>
          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>借出时间</Text>
            <Text style={styles.rightRight}>{book.borrow_time}</Text>
          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>归还时间</Text>
            <Text style={styles.rightRight}>{book.return_time}</Text>
          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>借书人</Text>
            <Text style={styles.rightRight}>{book.nickname}</Text>
          </View>
        </View>
      </View>
    )
  }
}

class InfoPartOrder extends React.Component {
  constructor (props) {
    super(props)
  }

  render () {
    let book = this.props.book
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
            <Text style={styles.rightRight}>{book.title}</Text>
          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>书籍编号</Text>
            <Text style={styles.rightRight}>{book.book_id}</Text>

          </View>
          <View style={styles.rightRow}>
            <Text style={styles.rightLeft}>借书人</Text>
            <Text style={styles.rightRight}>{book.nickname}</Text>
          </View>
        </View>
      </View>
    )
  }
}

class PayPart extends React.Component {
  render () {
    let price = this.props.price
    let time = new Date()
    return (
      <View style={styles.payContainer}>
        <View style={styles.payRow}>
          <Text style={styles.payLeft}>价格</Text>
          <Text style={styles.payRight}>{price}</Text>
        </View>
        <View style={styles.payRow}>
          <Text style={styles.payLeft}>支付时间</Text>
          <Text style={styles.payRight}>{time.getFullYear()}-{time.getMonth()}-{time.getDate()}</Text>
        </View>
      </View>
    )
  }
}

class ConfirmBtn extends React.Component {
  constructor (props) {
    super(props)
  }
  confirm = () => {
    let btnThis = this
    if (this.props.type === 'borrow') {
      async function getIt() {
        try {
          let response = await fetch(confirmBorrow + btnThis.props.pay_id, {
            method: 'GET',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            credentials: 'include',
          })
          let res  = await response.json()
          if (response.status >= 200 && response.status < 400) {
            Toast.show({
              supportedOrientations: ['portrait','landscape'],
              text: '确认成功',
              position: 'bottom',
              buttonText: 'Okay'
            })
          } else {
            console.log('Toast before')
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
        }
      }
      getIt()
    } else if (this.props.type === 'return') {
      let btnThis = this
      let form = {id_list: this.props.id_list, return_id: this.props.return_id}
      async function getIt () {
        try {
          let response = await fetch(confirmReturn, {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(form)
          })
          let res  = await response.json()
          console.log(res);
          if (response.status >= 200 && response.status < 400) {
            // btnThis.setState(toast, {show: true, word: '确认成功'})
            Toast.show({
              supportedOrientations: ['portrait','landscape'],
              text: '确认成功',
              position: 'bottom',
              buttonText: 'Okay'
            })
          } else {
            console.log('Toast before')
            // btnThis.setState(toast, {show: true, word: res})
            Toast.show({
              supportedOrientations: ['portrait','landscape'],
              text: '错误',
              position: 'bottom',
              buttonText: 'Okay'
            })
          }
        } catch(err) {
          console.log(err)
          // btnThis.setState(toast, {show: true, word: err})
          Toast.show({
            supportedOrientations: ['portrait','landscape'],
            text: '错误',
            position: 'bottom',
            buttonText: 'Okay'
          })
        }
      }
      getIt()
    } else if (this.props.type = 'order') {
      let btnThis = this
      let form = { order_id: this.props.order_id}
      async function getIt () {
        try {
          let response = await fetch(confirmOrder, {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            credentials: 'include',
            body: JSON.stringify(form)
          })
          console.log(JSON.stringify(form));
          let res  = await response.json()
          console.log(res);
          if (response.status >= 200 && response.status < 400) {
            Toast.show({
              supportedOrientations: ['portrait','landscape'],
              text: '确认成功',
              position: 'bottom',
              buttonText: 'Okay'
            })
          } else {
            console.log('Toast before')
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
        }
      }
      getIt()
    }
  }

  render () {
    return (
      <View style={styles.confirmContainer}>
        <Button info rounded onPress={this.confirm}>
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
