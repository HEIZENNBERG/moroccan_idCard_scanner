// firebaseConfig.js
import { initializeApp } from "firebase/app";
import 'firebase/compat/firestore';
import firebase from 'firebase/compat/app';
import 'firebase/compat/firestore';
const firebaseConfig = {
    apiKey: "AIzaSyDsp8TN_JU-u2TI7zmE2lzOMcf3TuxY67w",
    authDomain: "idcards-5a7d0.firebaseapp.com",
    projectId: "idcards-5a7d0",
    storageBucket: "idcards-5a7d0.appspot.com",
    messagingSenderId: "377512360243",
    appId: "1:377512360243:web:cf793d2ac779e08f436646",
    measurementId: "G-M111NBG7BR"
  };

if (!firebase.apps.length) {
  firebase.initializeApp(firebaseConfig);
}

const firestore = firebase.firestore();
export { firebase, firestore };
