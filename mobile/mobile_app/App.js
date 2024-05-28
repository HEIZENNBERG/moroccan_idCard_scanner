import React, { useEffect } from 'react';
import { StatusBar } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import FirstPage from './components/first';
import SplashScreen from './components/splash'; // Import SplashScreen component

const Stack = createStackNavigator();

const App = () => {

  return (
    <>
    <StatusBar hidden={false} />
    <NavigationContainer>
      <Stack.Navigator>
        <Stack.Screen name="s" component={SplashScreen}  options={{ headerShown: false }}/>
        <Stack.Screen name="FirstPage" component={FirstPage}  options={{ headerShown: false }}/>
      </Stack.Navigator>
    </NavigationContainer>
    </>
  );
};

export default App;
