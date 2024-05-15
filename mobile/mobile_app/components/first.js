import React, { useState, useEffect } from 'react';
import {ScrollView, View, Button, Alert, Text, Image, StyleSheet } from 'react-native';
import * as FileSystem from "expo-file-system";
import { DataTable } from 'react-native-paper'; 


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

  const delete_uri = () => {
    setPhotoUris([null, null]);
  }

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
    <ScrollView style={{ flex:1}}>
      <View style={styles.container}>

        <View style={styles.scannerContainer}>
          <View style={styles.imageContainer}>
            <Image source={{ uri: photoUris[0] }} 
                  style={[styles.image, {marginRight: 10}]} />
            <Image source={{ uri: photoUris[1] }} style={styles.image} />
          </View>

          <View style={styles.buttonContainer}>
            <View style={{marginLeft : 20}}>
              <Button title="Scan" onPress={handleScanPress}  color ="rgb(71, 209, 71)" style={[styles.button]}/>
            </View>
            <View style={{marginLeft : 20}}>
              <Button title='delete images' onPress={delete_uri} color ="rgb(71, 209, 71)" style={[styles.button]}/>
            </View>
          </View>
          <Button title="Process Imgs" titleStyle={{color : "black"}} onPress={toServer} color ="rgb(71, 209, 71)" style={styles.button} />
        
        <View style={styles.tableContainer}>
            <DataTable style={styles.table}> 
              <DataTable.Header style={styles.tableHeader}> 
                <DataTable.Title>feild</DataTable.Title> 
                <DataTable.Title>value</DataTable.Title> 

              </DataTable.Header> 
              <DataTable.Row style={styles.row}> 
                <DataTable.Cell>first Name</DataTable.Cell> 
                <DataTable.Cell>Dosa</DataTable.Cell> 
              </DataTable.Row> 
              <DataTable.Row> 
                <DataTable.Cell>Second Name</DataTable.Cell> 
                <DataTable.Cell>Dosa</DataTable.Cell> 
              </DataTable.Row>
              <DataTable.Row style={styles.row}> 
                <DataTable.Cell>Day of Birth</DataTable.Cell> 
                <DataTable.Cell>Dosa</DataTable.Cell> 
              </DataTable.Row>
              <DataTable.Row> 
                <DataTable.Cell>City of Birth</DataTable.Cell> 
                <DataTable.Cell>Dosa</DataTable.Cell> 
              </DataTable.Row> 
              <DataTable.Row style={styles.row}> 
                <DataTable.Cell>CIN</DataTable.Cell> 
                <DataTable.Cell>Dosa</DataTable.Cell> 
              </DataTable.Row>
              <DataTable.Row> 
                <DataTable.Cell>Father Name</DataTable.Cell> 
                <DataTable.Cell>Dosa</DataTable.Cell> 
              </DataTable.Row>
              <DataTable.Row style={styles.row}> 
                <DataTable.Cell>Mother Name</DataTable.Cell> 
                <DataTable.Cell>Dosa</DataTable.Cell> 
              </DataTable.Row>    
              <DataTable.Row> 
                <DataTable.Cell>Home Adress</DataTable.Cell> 
                <DataTable.Cell>Dosa</DataTable.Cell> 
              </DataTable.Row> 
              <DataTable.Row style={styles.row}> 
                <DataTable.Cell>gender</DataTable.Cell> 
                <DataTable.Cell>Dosa</DataTable.Cell> 
              </DataTable.Row>       
            </DataTable> 
          </View>
          <Button title="Save informations" titleStyle={{color : "black"}}  color ="rgb(71, 209, 71)" style={[styles.button, {Bottom: 20}]} />

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
  scannerContainer:{
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
    height : 200,
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
  process:{
    height : 50,
    width : '100%',
    position : 'absolute',
    bottom : 0,
    backgroundColor : "grey",
  },
  row:{
    backgroundColor : 'rgb(217, 217, 217)'
  }
});

export default FirstPage;
