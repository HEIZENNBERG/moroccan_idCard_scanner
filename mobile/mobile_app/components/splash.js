// SplashScreen.js

import React, { useEffect } from 'react';
import { Image, StyleSheet, View, Text } from 'react-native';

const SplashScreen = ({ navigation }) => {
  useEffect(() => {
    // Simulate a delay or perform any necessary initialization tasks
    setTimeout(() => {
      // Navigate to the main screen
      navigation.navigate('FirstPage');
    }, 1); // 3000 milliseconds (3 seconds) delay
  }, []);

  return (
    <View style={styles.container}>
        <Image
        source={require('../assets/leet.png')}
        style={styles.leet_logo}
      />
      <Image
        source={require('../assets/scan_card.png')}
        style={styles.splash}
      />
      {/* Use the system font with fontStyle: 'italic' for math italic style */}
      <Text style={[styles.title, {fontStyle: 'italic'}]}>
        Moroccan card-Id Scanner
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: 'white',
  },
  leet_logo: {
    width: 100,
    height: 100,
    position: 'absolute',
    top: 20,
    left: 20,
  },
  splash: {
    width: 250,
    height: 200,
    resizeMode: 'contain',
  },
  title:{
    fontSize : 25,
    fontWeight: "bold",
    color :"rgb(71, 209, 71)"
  }
});

export default SplashScreen;
