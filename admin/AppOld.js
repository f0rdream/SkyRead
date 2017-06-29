import React from 'react';
import {
  AppRegistry,
  Text,
  View,
  Button,
  Dimensions,
  StyleSheet,
  TouchableHighlight,
  Image,
} from 'react-native';
import { StackNavigator, TabNavigator } from 'react-navigation';
import Camera from 'react-native-camera';

// The home page
class HomeScreen extends React.Component {
  static navigationOptions = {
    title: '图书管理员',
  };
  render() {
    const { navigate } = this.props.navigation;
    return (
      <View style={{flex: 1}}>
        <View>
          <Image source={{uri: 'https://facebook.github.io/react/img/logo_og.png'}} style={{width: 150, height: 150}} />
          <Text>ID:9527</Text>
          <Button title="签到"/>
        </View>
        <View>
          <Button
            onPress={() => navigate('Scan')}
            title="扫码"/>
        </View>
      </View>
    )
  }
}

class ScanScreen extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      QRResult: ''
    };
  }
  static navigationOptions = {
    title: '扫码',
  };
  render() {
    const { navigate } = this.props.navigation;
    return (
      <View style={styles.container}>
        <Camera
          ref={(cam) => {
            this.camera = cam;
          }}
          style={styles.preview}
          aspect={Camera.constants.Aspect.fill}
          onBarCodeRead={this.getQR.bind(this)}>
        </Camera>
      </View>
    )
  }

  getQR(data, bounds) {
    this.setState(preState => {
      return { QRResult: data }
    })
    console.log(data)
  }
}

class ChatScreen extends React.Component {
  static navigationOptions = ({ navigation }) => ({
    title: `Chat with ${navigation.state.params.user}`,
  });
  render() {
    const { params } = this.props.navigation.state;
    return (
      <View>
        <Text>Chat with {params.user}</Text>
      </View>
    )
  }
}

class RecentChatsScreen extends React.Component {
  render() {
    return (
      <View style={{flex: 1}}>
        <BadInstagramCloneApp></BadInstagramCloneApp>
      </View>
    )
  }
}
class AllContactsScreen extends React.Component {
  render() {
    return <Text>List of all contacts</Text>
  }
}

// The Camera Area
class BadInstagramCloneApp extends React.Component {
  render() {
    return (
      <View style={styles.container}>
        <Camera
          ref={(cam) => {
            this.camera = cam;
          }}
          style={styles.preview}
          aspect={Camera.constants.Aspect.fill}
          onBarCodeRead={this.getQR.bind(this)}>
          <Text style={styles.capture} onPress={this.takePicture.bind(this)}>[CAPTURE]</Text>
        </Camera>
      </View>
    );
  }

  takePicture() {
    const options = {};
    //options.location = ...
    this.camera.capture({metadata: options})
      .then((data) => console.log(data))
      .catch(err => console.error(err));
  }

  getQR(data, bounds) {
    console.log(data)
  }
}
const MainScreenNavigator = TabNavigator({
  Recnet: { screen: RecentChatsScreen },
  All: { screen: AllContactsScreen },
});

const cliReact = StackNavigator({
  Home: { screen: HomeScreen },
  Scan: { screen: ScanScreen },
});
MainScreenNavigator.navigationOptions = {
  title: 'My Chats',
};






// Styles
const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: 'row',
  },
  preview: {
    flex: 1,
    justifyContent: 'flex-end',
    alignItems: 'center'
  },
  capture: {
    flex: 0,
    backgroundColor: '#fff',
    borderRadius: 5,
    color: '#000',
    padding: 10,
    margin: 40
  }
});
