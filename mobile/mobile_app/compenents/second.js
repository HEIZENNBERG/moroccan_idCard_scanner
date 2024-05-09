import React, { useState, useEffect } from 'react';
import { View, Button, Text, Image, StyleSheet } from 'react-native';
import { Camera } from 'expo-camera';

const SecondPage = ({ navigation }) => {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraVar, setCameraVar] = useState(null);
  const [imageUri, setImageUri] = useState(null);

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (cameraVar ) {
      const { uri } = await cameraVar.takePictureAsync();
      setImageUri(uri);
      navigation.navigate('FirstPage', { photoUri: uri });
    }
  };

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={{ flex: 1 }}>
      <Camera
        style={{ flex: 1 }}
        type={Camera.Constants.Type.back}
        ref={ref => setCameraVar(ref)}
      />
      {/* Rectangle overlay */}
      <View style={styles.overlay}>
        <View style={styles.rectangle} />
      </View>
      <View style={{ flexDirection: 'row', justifyContent: 'center', marginBottom: 20 }}>
        <Button title="Take Picture" onPress={takePicture} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  overlay: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
  },
  rectangle: {
    height: 200, // Adjust height as needed
    width: 300, // Adjust width as needed
    borderWidth: 2,
    borderColor: 'green',
    backgroundColor: 'transparent',
  },
});

export default SecondPage;
