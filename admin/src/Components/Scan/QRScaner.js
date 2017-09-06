import React from 'react'
import { Container, Toast } from 'native-base'
import { StyleSheet, View, TextInput, TouchableOpacity, Text, Image } from 'react-native'
import Camera from 'react-native-camera'


export default class QRScaner extends React.Component {
  static propTypes = {
    onPressCancel: React.PropTypes.func,
    onQRRead: React.PropTypes.func,
    cancelButtonVisible: React.PropTypes.bool,
    cancelButtonTitle: React.PropTypes.string
  }
  static defaultProps = {
    cancelButtonVisible: false,
    cancelButtonTitle: '取消'
   }

   constructor (props) {
     super(props)
   }

  _onPressCancel = () => {
    this.props.onPressCancel()
  }

  _onQRRead =  (data) => {
    this.props.onQRRead(data)
  }

  render () {
    let cancelButton = null;

    if (this.props.cancelButtonVisible) {
      cancelButton = <CancelButton onPress={this._onPressCancel} title={this.props.cancelButtonTitle} />;
    }

    return (
      <Container>
        <Camera
          ref={(cam) => {this.camera = cam}}
          style={styles.camera}
          aspect={Camera.constants.Aspect.fit}
          onBarCodeRead={this._onQRRead}
          >
          <View style={styles.rectangleContainer}>
            <View style={styles.rectangle}/>
          </View>
          { cancelButton }
        </Camera>
      </Container>
    )
  }
}

class CancelButton extends React.Component {
  render () {
    return (
      <View style={styles.cancelButton}>
        <TouchableOpacity onPress={this.props.onPress}>
          <Text style={styles.cancelButtonText}>{this.props.title}</Text>
        </TouchableOpacity>
      </View>
    )
  }
}

// var CancelButton = React.createClass({
//   render: function() {
//     return (
//       <View style={styles.cancelButton}>
//         <TouchableOpacity onPress={this.props.onPress}>
//           <Text style={styles.cancelButtonText}>{this.props.title}</Text>
//         </TouchableOpacity>
//       </View>
//     );
//   },
// });

const styles = StyleSheet.create({
  // container: {
  //   flex: 1,
  //   flexDirection: 'row',
  // },
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
  // },
  camera: {
    flex: 1,
    alignItems: 'center',
  },

  rectangleContainer: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
  },

  rectangle: {
    height: 250,
    width: 250,
    borderWidth: 2,
    borderColor: '#00FF00',
    backgroundColor: 'transparent',
  },

  cancelButton: {
    flexDirection: 'row',
    justifyContent: 'center',
    backgroundColor: 'white',
    borderRadius: 3,
    padding: 15,
    width: 100,
    bottom: 10,
  },
  cancelButtonText: {
    fontSize: 17,
    fontWeight: '500',
    color: '#0097CE',
  },
})

// var QRCodeScreen = React.createClass({
//
//   propTypes: {
//     cancelButtonVisible: React.PropTypes.bool,
//     cancelButtonTitle: React.PropTypes.string,
//     onSucess: React.PropTypes.func,
//     onCancel: React.PropTypes.func,
//   },
//
//   getDefaultProps: function() {
//     return {
//       cancelButtonVisible: false,
//       cancelButtonTitle: 'Cancel',
//     };
//   },
//
//   _onPressCancel = () => {
//
//   },
//
//   _onQRRead =  (data) => {
//     this.props.onQRRead(data)
//   },
//
//   render: function() {
//     var cancelButton = null;
//     this.barCodeFlag = true;
//
//     if (this.props.cancelButtonVisible) {
//       cancelButton = <CancelButton onPress={this._onPressCancel} title={this.props.cancelButtonTitle} />;
//     }
//
//     return (
//       <Camera onBarCodeRead={this._onQRRead} style={styles.camera}>
//         <View style={styles.rectangleContainer}>
//           <View style={styles.rectangle}/>
//         </View>
//         {cancelButton}
//       </Camera>
//     );
//   },
// });
//
// var CancelButton = React.createClass({
//   render: function() {
//     return (
//       <View style={styles.cancelButton}>
//         <TouchableOpacity onPress={this.props.onPress}>
//           <Text style={styles.cancelButtonText}>{this.props.title}</Text>
//         </TouchableOpacity>
//       </View>
//     );
//   },
// });
//
// var styles = StyleSheet.create({
//
//   camera: {
//     height: 568,
//     alignItems: 'center',
//   },
//
//   rectangleContainer: {
//     flex: 1,
//     alignItems: 'center',
//     justifyContent: 'center',
//     backgroundColor: 'transparent',
//   },
//
//   rectangle: {
//     height: 250,
//     width: 250,
//     borderWidth: 2,
//     borderColor: '#00FF00',
//     backgroundColor: 'transparent',
//   },
//
//   cancelButton: {
//     flexDirection: 'row',
//     justifyContent: 'center',
//     backgroundColor: 'white',
//     borderRadius: 3,
//     padding: 15,
//     width: 100,
//     bottom: 10,
//   },
//   cancelButtonText: {
//     fontSize: 17,
//     fontWeight: '500',
//     color: '#0097CE',
//   },
// });
//
// module.exports = QRCodeScreen;
