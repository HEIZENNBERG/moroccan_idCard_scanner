import React, { useState, useEffect } from 'react';
import { View, Button, Alert, Text, Image, StyleSheet } from 'react-native';
import * as FileSystem from "expo-file-system";

const FirstPage = ({ navigation, route }) => {
  const [photoUris, setPhotoUris] = useState([null, null]); // Two URI slots

  // Extract the photoUri parameter from the route if available
  const { photoUri } = route.params || {};

  const uriToBase64 = async (uri) => {
    try {
      const base64 = await FileSystem.readAsStringAsync(uri, {
        encoding: FileSystem.EncodingType.Base64,
      });
      return base64;
    } catch (error) {
      console.error("Error converting URI to base64:", error);
      return undefined;
    }
  };

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

  const toServer = async () => {
    const schema = "http://";
    const host = "10.32.103.197";
    const route = "/image";
    const port = "5000";
    const url = `${schema}${host}:${port}${route}`;
  
    // Convert URIs to base64
    const base64Images = await Promise.all(photoUris.map(async (uri) => {
      if (uri) {
        return await uriToBase64(uri);
      }
    }));
  
    // Filter out undefined values
    const validBase64Images = base64Images.filter(image => image !== undefined);
  
    // Send base64 images to the server
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ images: validBase64Images }), // Sending an array of base64 images
      });
      console.log(await response.json());
    } catch (error) {
      console.error("Error sending images to server:", error);
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Stored URIs:</Text>
      {photoUris.map((uri, index) => (
        <Image key={index} source={{ uri: uri }} style={{ width: 200, height: 200, marginVertical: 10 }} />
      ))}
      <Button title="Scan" onPress={handleScanPress} style={styles.button}/>
      <Button title="Process Imgs" onPress={toServer} style={styles.button} />
    </View>
  );
};

const styles = StyleSheet.create({
  button:{
    marginBottom: 15,
  }
});


export default FirstPage;
