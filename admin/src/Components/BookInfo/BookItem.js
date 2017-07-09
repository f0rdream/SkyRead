export default class BookItem extends React.Component {
  constructor(props) {
    super(props)
  }

  render () {
    return ()
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
