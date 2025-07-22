<template>
  <div class="container flex">
    <!-- Error Message Display -->
    <template v-if="errors.length > 0">
      <div class="error-container flex" :class="{ showError: showError }">
        <p style="font-size: 1.3vw;" v-for="error in errors" :key="error" class="error-message">{{ error }}</p>
      </div>
    </template>

    <!-- Success Message Display -->
    <template v-if="successMessage.length > 0">
      <div class="success-container flex" :class="{ showSuccess: showSuccess }">
        <p style="font-size: 1.3vw;" v-for="message in successMessage" :key="message" class="success-message">{{ message }}</p>
      </div>
    </template>

    <div class="signUp flex">
      <h1>SCRAPY</h1>
      <div class="joinText flex">
        <p>Join the Scrapy family</p>
        <p>Already have an account? <router-link :to="{ 'name': 'Login' }"><u>Log in to your account</u></router-link></p>
      </div>
      <form v-on:submit.prevent="submitForm">
        <div class="name flex">
          <input type="text" v-model="form.firstName" placeholder="First Name" />
          <input type="text" v-model="form.lastName" placeholder="Last Name">
        </div>

        <div class="password flex">
          <input type="email" v-model="form.email" placeholder="Email">
          <input type="password" v-model="form.password1" placeholder="Password">
          <input type="password" v-model="form.password2" placeholder="Confirm Password">
          <input type="text" v-model="form.city" placeholder="City">
          <input type="text" v-model="form.number" placeholder="Mobile Number">
          <button>CONTINUE</button>
        </div>
      </form>
    </div>

    <hr class="vertical-hr">
    <div class="signUpText flex" style="flex-direction: column;">
      EVERY PIECE HAS A PURPOSE. LET'S REPURPOSE TOGETHER!
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { useToastStore } from '@/stores/toast.js'

export default {
  name: 'SignUp',
  setup() {
    const toastStore = useToastStore()
    return { toastStore }
  },

  data() {
    return {
      form: {
        email: '',
        firstName: '',
        lastName: '',
        number: '',
        city: '',
        password1: '',
        password2: ''
      },
      errors: [],
      successMessage: [],
      showError: false,
      showSuccess: false,
    }
  },

  methods: {
    submitForm() {
      console.log("Submit form called");

      // Reset errors if the form is being resubmitted
      this.errors = [] // Reset the errors
      this.successMessage = [] // Reset success messages
      this.showError = true; // Show errors immediately
      this.showSuccess = false; // Hide success message initially

      // Validation checks
      if (this.form.email === '') {
        this.errors.push('Your e-mail is missing')
      }
      if (this.form.firstName === '') {
        this.errors.push('Your first name is missing')
      }
      if (this.form.lastName === '') {
        this.errors.push('Your last name is missing')
      }
      if (this.form.number === '') {
        this.errors.push('Your number is missing')
      }
      if (this.form.password1 === '') {
        this.errors.push('Your password is missing')
      }
      if (this.form.password1 !== this.form.password2) {
        this.errors.push('The password does not match')
      }

      // If there are no errors, submit the form
      if (this.errors.length === 0) {
        console.log("Form data is valid, sending request...");
        axios
          .post('/api/signup/', this.form)
          .then(response => {
            console.log("Response received:", response);
            if (response.data.message === 'success') {
              // Display success message
              this.successMessage.push('Account successfully made! Please log in.')
              this.showSuccess = true; // Show success message

              // Hide the success message after 7 seconds
              setTimeout(() => {
                this.showSuccess = false;
              }, 7000);

              // Redirect after success
              this.$router.push('/Login');
            } else if (response.data.error === 'Email is already taken') {
              this.errors.push('The email is already taken');
            } else {
              this.toastStore.showToast(5000, 'Something went wrong. Please try again', 'bg-red');
            }
          })
          .catch(error => {
            console.log("Error during signup:", error);
            if (error.response && error.response.data.error) {
              if (error.response.data.error === 'Email is already taken') {
                this.errors.push('The email is already taken');
              } else {
                this.errors.push('An unexpected error occurred');
              }
            }
          })
      }

      // Show error messages and hide them after 7 seconds
      if (this.errors.length > 0) {
        setTimeout(() => {
          this.showError = false; // Hide the error after 7 seconds
        }, 7000);
      }
    },

    resetForm() {
      this.form.email = ''
      this.form.firstName = ''
      this.form.lastName = ''
      this.form.number = ''
      this.form.password1 = ''
      this.form.password2 = ''
    }
  }
}
</script>

<style scoped>
.container {
  width: 100vw;
  height: 100vh;
  gap: 2vw;
}

.signUp {
  width: 49vw;
  height: 100vh;
  flex-direction: column;
  position: relative;
}

h1 {
  position: relative;
  color: lightgreen;
  font-family: "Concert One", serif;
  bottom: 5vh;
  font-size: 7vw;
}

.name {
  gap: 1vw;
}

.name input {
  border: 1px solid rgb(147, 147, 147);
  width: 13vw;
  height: 6vh;
  border-radius: 30px;
  padding: 10px;
  outline: none;
}

.password {
  flex-direction: column;
  gap: 2vh;
  position: relative;
  top: 2vh;
}

.password input {
  border: 1px solid rgb(147, 147, 147);
  outline: none;
  width: 27vw;
  border-radius: 30px;
  height: 7vh;
  padding: 10px;
}

.password button {
  width: 10vw;
  height: 8vh;
  border: 3px solid black;
  border-radius: 40px;
  cursor: pointer;
  transition: transform 0.2s;
  background-color: #8db161;
  color: white;
  font-family: "Concert One", serif;
  font-size: 1.5vw;
}

.password button:hover {
  transform: scale(1.05);
  background-color: white;
  color: lightgreen;
  border: 1px solid rgb(196, 196, 196);
}

.signUpText {
  width: 49vw;
  height: 100vh;
  color: lightgreen;
  font-family: "Concert One", serif;
  font-size: 5vw;
}

.vertical-hr {
  width: 1px;
  height: 90vh;
  background-color: rgb(228, 228, 228);
  border: none;
  margin: 0;
}

.joinText {
  flex-direction: column;
  position: relative;
  bottom: 6vh;
}

/* Error message styling */
.error-container {
  position: absolute;
  top: 20px; /* Position the error message near the top */
  left: 50%; /* Center horizontally */
  transform: translateX(-50%); /* Adjust the positioning to exactly center */
  padding: 15px;
  background-color: #f8d7da;
  border-radius: 5px;
  z-index: 999;
  opacity: 0; /* Initially hidden */
  animation: fadeInOut 7s ease-in-out forwards;
  width: 30vw;
  flex-direction: column;
}

/* Success message styling */
.success-container {
  position: absolute;
  top: 20px; /* Position the success message near the top */
  left: 50%; /* Center horizontally */
  transform: translateX(-50%); /* Adjust the positioning to exactly center */
  padding: 15px;
  background-color: #d4edda; /* Green background for success */
  border-radius: 5px;
  z-index: 999;
  opacity: 0; /* Initially hidden */
  animation: fadeInOut 7s ease-in-out forwards;
  width: 30vw;
  flex-direction: column;
}

/* Apply showError class when error is visible */
.error-container.showError, .success-container.showSuccess {
  opacity: 1;
}

.error-message, .success-message {
  color: #721c24; /* Error color */
  font-size: 1.1rem;
  margin: 5px 0;
  font-weight: 600;
}

/* Keyframes for fade-in and fade-out */
@keyframes fadeInOut {
  0% {
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    opacity: 0;
  }
}
</style>
