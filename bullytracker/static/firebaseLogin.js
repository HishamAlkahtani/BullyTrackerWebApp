import { initializeApp } from "https://www.gstatic.com/firebasejs/10.14.1/firebase-app.js";
import {
  getAuth,
  signInWithEmailAndPassword,
  /*setPersistence,
  browserLocalPersistence,
  browserSessionPersistence,
  inMemoryPersistence,*/
} from "https://www.gstatic.com/firebasejs/10.14.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyCfhnTKzt42gaUtVzb6Rp9YrE4HRRGnG04",

  authDomain: "bully-tracker-4476f.firebaseapp.com",

  projectId: "bully-tracker-4476f",

  storageBucket: "bully-tracker-4476f.appspot.com",

  messagingSenderId: "726401397837",

  appId: "1:726401397837:web:a9a6d6489533880aa79804",
};

const app = initializeApp(firebaseConfig);

const auth = getAuth(app);

// Session cookie will be set by flask in the backend, so no need
// for firebase to store anything client-side
// ↓ idk why this is not working ↓ fix it later (I hope it doesnt break anything)
// setPersistence(inMemoryPersistence)

// Function to be called when login button is pressed
function loginButtonClicked() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  signInWithEmailAndPassword(auth, username, password)
    .then((user) => {
      return user.user.getIdToken().then((idtoken) => {
        // TODO: Do stuff with idtoken (POST it to backend)
        document.getElementById("idtokenInput").value = idtoken;
        document.getElementById("loginForm").submit();
      });
    })
    .catch((error) => {
      alert(error);
    });
}

document
  .getElementById("loginButton")
  .addEventListener("click", loginButtonClicked);
