import React, { useState, useEffect } from 'react';
import { View, Button, Text, StyleSheet } from 'react-native';
import { Camera } from 'expo-camera';

const SecondPage = ({ navigation }) => {
  const [hasPermission, setHasPermission] = useState(null);
  const [cameraVar, setCameraVar] = useState(null);
  const [imageUri, setImageUri] = useState(null);
  const [torchOn, setTorchOn] = useState(false); // State variable for torch

  useEffect(() => {
    (async () => {
      const { status } = await Camera.requestCameraPermissionsAsync();
      setHasPermission(status === 'granted');
    })();
  }, []);

  const takePicture = async () => {
    if (cameraVar) {
      try {
        const { uri } = await cameraVar.takePictureAsync();
        setImageUri(uri);
        navigation.navigate('FirstPage', { photoUri: uri });
      } catch (error) {
        console.error('Error taking picture:', error);
      }
    }
  };

  const toggleFlashlight = () => {
    if (cameraVar) {
      if (cameraVar.setTorchModeAsync) { // Check if the function is available
        try {
          const newTorchState = !torchOn;
          cameraVar.setTorchModeAsync(newTorchState ? Camera.Constants.FlashMode.torch : Camera.Constants.FlashMode.off);
          setTorchOn(newTorchState);
        } catch (error) {
          console.error('Error toggling flashlight:', error);
        }
      } else {
        console.warn("Torch mode control is not supported on this device.");
      }
    }
  };

  if (hasPermission === null) {
    return <View />;
  }
  if (hasPermission === false) {
    return <Text>No access to camera</Text>;
  }

  return (
    <View style={styles.container}>
      <Camera
        style={styles.camera}
        type={Camera.Constants.Type.back}
        ref={ref => setCameraVar(ref)}
      />
      {/* Rectangle overlay */}
      <View style={styles.overlay}>
        <View style={styles.rectangle} />
      </View>
      <View style={styles.buttonContainer}>
        <Button title="Take Picture" color="rgb(71, 209, 71)" onPress={takePicture} />
        <Button
          title={torchOn ? "Turn Flashlight Off" : "Turn Flashlight On"}
          color="rgb(71, 209, 71)"
          onPress={toggleFlashlight}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: 'black',
  },
  camera: {
    flex: 1,
  },
  overlay: {
    ...StyleSheet.absoluteFillObject,
    justifyContent: 'center',
    alignItems: 'center',
  },
  rectangle: {
    height: 200,
    width: 300,
    borderWidth: 2,
    borderColor: 'green',
    backgroundColor: 'transparent',
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
  },
});

export default SecondPage;
