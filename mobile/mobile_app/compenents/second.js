import React, { useState, useEffect } from 'react';
import { View, Button, Text, Image } from 'react-native';
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
      <View style={{ flexDirection: 'row', justifyContent: 'center', marginBottom: 20 }}>
        <Button title="Take Picture" onPress={takePicture} />
      </View>
    </View>
  );
};

export default SecondPage;
