import React, { useState, useEffect } from 'react';
import { View, Button, Alert, Text, Image } from 'react-native';

const FirstPage = ({ navigation, route }) => {
  const [photoUris, setPhotoUris] = useState([null, null]); // Two URI slots

  // Extract the photoUri parameter from the route if available
  const { photoUri } = route.params || {};

  // Update photoUris state when a new URI is received
  useEffect(() => {
    if (photoUri) {
      setPhotoUris(prevUris => {
        const updatedUris = [...prevUris];
        const index = updatedUris.findIndex(uri => uri === null);
        if (index !== -1) {
          updatedUris[index] = photoUri;
        }
        return updatedUris;
      });
    }
  }, [photoUri]);

  const handleScanPress = () => {
    if (photoUris.every(uri => uri !== null)) {
      Alert.alert('Maximum Photos Reached', 'You can only store up to 2 photos.');
    } else {
      navigation.navigate('SecondPage');
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Stored URIs:</Text>
      {photoUris.map((uri, index) => (
        <Image key={index} source={{ uri: uri }} style={{ width: 200, height: 200, marginVertical: 10 }} />
      ))}
      <Button title="Scan" onPress={handleScanPress} />
    </View>
  );
};

export default FirstPage;
