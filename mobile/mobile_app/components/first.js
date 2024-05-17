import React, { useState, useEffect } from 'react';
import { ScrollView, View, Button, Alert, Text, Image, StyleSheet, ActivityIndicator } from 'react-native';
import * as FileSystem from "expo-file-system";
import { DataTable } from 'react-native-paper';
import { firebase, firestore } from './firebase';

const FirstPage = ({ navigation, route }) => {
  const [photoUris, setPhotoUris] = useState([null, null]);
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);

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

  const deleteUri = () => {
    setPhotoUris([null, null]);
    setResults(null);
  };

  const toServer = async () => {
    setLoading(true);
    const schema = "http://";
    const host = "10.32.103.197";
    const route = "/image";
    const port = "5000";
    const url = `${schema}${host}:${port}${route}`;

    const base64Images = await Promise.all(photoUris.map(async (uri) => {
      if (uri) {
        return await uriToBase64(uri);
      }
    }));

    const validBase64Images = base64Images.filter(image => image !== undefined);

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ images: validBase64Images }), 
      });
      const responseData = await response.json();
      setResults(responseData.results); 
    } catch (error) {
      Alert.alert('An error has occurred, please try again.');
      console.error("Error sending images to server:", error);
    } finally {
      setLoading(false);
    }
  };

  const saveInformation = async () => {
    if (!results) return;

    try {
      const docRef = await firestore.collection('id_informations').add({
        timestamp: firebase.firestore.FieldValue.serverTimestamp(),
        results,
      });
      Alert.alert('Success', 'Information saved successfully.');
    } catch (error) {
      Alert.alert('Error', 'Failed to save information.');
      console.error("Error saving information to Firestore:", error);
    }
  };

  return (
    <ScrollView style={{ flex: 1 }}>
      <View style={styles.container}>
        <View style={styles.scannerContainer}>
          <View style={styles.imageContainer}>
            <Image source={{ uri: photoUris[0] }} style={[styles.image, { marginRight: 10 }]} />
            <Image source={{ uri: photoUris[1] }} style={styles.image} />
          </View>

          <View style={styles.buttonContainer}>
            <View style={{ marginLeft: 20 }}>
              <Button title="Scan" onPress={handleScanPress} color="rgb(71, 209, 71)" style={[styles.button]} />
            </View>
            <View style={{ marginLeft: 20 }}>
              <Button title='Delete Images' onPress={deleteUri} color="rgb(71, 209, 71)" style={[styles.button]} />
            </View>
          </View>
          <Button title="Process Imgs" titleStyle={{ color: "black" }} onPress={toServer} color="rgb(71, 209, 71)" style={styles.button} />
          {loading && (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color="rgb(71, 209, 71)" />
            </View>
          )}
          {results && (
            <View style={styles.tableContainer}>
              <DataTable style={styles.table}>
                <DataTable.Header style={styles.tableHeader}>
                  <DataTable.Title>Field</DataTable.Title>
                  <DataTable.Title>Value</DataTable.Title>
                </DataTable.Header>
                {results.map((result, resultIndex) => (
                  Object.entries(result).map(([key, value], entryIndex) => (
                    <DataTable.Row key={`${resultIndex}-${entryIndex}`} style={styles.row}>
                      <DataTable.Cell>{key}</DataTable.Cell>
                      <DataTable.Cell>{value}</DataTable.Cell>
                    </DataTable.Row>
                  ))
                ))}
              </DataTable>
              <Button title="Save Information" titleStyle={{ color: "black" }} onPress={saveInformation} color="rgb(71, 209, 71)" style={[styles.button, { marginBottom: 20 }]} />
            </View>
          )}
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F0F0F0',
  },
  scannerContainer: {
    marginTop: 10,
  },
  imageContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: 'white',
    paddingHorizontal: 20,
    paddingVertical: 10,
    borderRadius: 10,
    marginVertical: 10,
    height: 200,
  },
  image: {
    width: 150,
    height: 180,
    borderRadius: 10,
  },
  tableContainer: {
    marginTop: 20,
  },
  table: {
    borderRadius: 5,
    marginBottom: 20,
  },
  buttonContainer: {
    justifyContent: 'center',
    flexDirection: 'row',
    marginBottom: 20,
    height: "auto",
  },
  button: {
    marginRight: 10,
    marginLeft: 10,
  },
  row: {
    backgroundColor: 'rgb(217, 217, 217)',
  }
});

export default FirstPage;
