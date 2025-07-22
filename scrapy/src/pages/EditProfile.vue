<template>
  <Navbar/>
  <h1>EDIT PROFILE</h1>
    <div class="edit-profile-container flex">
      <form @submit.prevent="saveProfile" class="edit flex">
        <label>FIRST NAME</label>
        <input v-model="editData.firstName" type="text" required />
  
        <label>LAST NAME</label>
        <input v-model="editData.lastName" type="text" required />
  
        <label>EMAIL</label>
        <input v-model="editData.email" type="email" required />
  
        <label>PHONE NUMBER</label>
        <input v-model="editData.number" type="text" />

        <label>CITY</label>
        <input v-model="editData.city" type="text" />
  
        <button type="submit">SAVE</button>
      
      </form>
  
      <!-- <h2>Change Password</h2> -->
      <form @submit.prevent="changePassword" class="edit flex">
        <label>CURRENT PASSWORD</label>
        <input v-model="passwordData.old_password" type="password" required />
  
        <label>NEW PASSWORD</label>
        <input v-model="passwordData.new_password" type="password" required />
  
        <label>CONFIRM NEW PASSWORD</label>
        <input v-model="passwordData.confirm_password" type="password" required />
  
        <button type="submit" >CONFIRM</button>
      </form>
    </div>
    <Footer/>
  </template>
  
  <script>
import Navbar from "@/layouts/Navbar.vue";
import Footer from '@/layouts/Footer.vue'
import axios from 'axios';
  
  export default {
    name: 'EditProfile',
    components:{
      Navbar,
      Footer
    },
    data() {
      return {
        editData: {
           
          firstName: '',
          lastName: '',
          email: '',
          number: '',
          city:''
        },
        passwordData: {
          old_password: '',
          new_password: '',
          confirm_password: ''
        }
      };
    },
    created() {
  const token = localStorage.getItem("user.access");
  axios.get("/api/profile/", {
    headers: { Authorization: `Bearer ${token}` }
  }).then(response => {
      console.log("Profile API Response:", response.data);
    const user = response.data.user || response.data;


    this.editData = {
      id: user.id,
      firstName: user.firstName,
      lastName: user.lastName,
      email: user.email,
      number: user.number,
      city: user.city
    };
  }).catch(err => {
    alert("Failed to load profile.");
  });
}
,
    methods: {
        async saveProfile() {
  const token = localStorage.getItem("user.access");
  try {
    await axios.put("/api/profile/", this.editData, {
      headers: { Authorization: `Bearer ${token}` }
    });
    alert("Profile updated!");
    this.$router.push(`/UserProfile/${this.editData.id}`);
  } catch (err) {
    alert("Update failed.");
  }
}
,
      async changePassword() {
        if (this.passwordData.new_password !== this.passwordData.confirm_password) {
          alert("New passwords do not match!");
          return;
        }
  
        const token = localStorage.getItem("user.access");
        try {
          const response = await axios.put("/api/profile/change-password/", {
            old_password: this.passwordData.old_password,
            new_password: this.passwordData.new_password
          }, {
            headers: { Authorization: `Bearer ${token}` }
          });
  
          alert(response.data.message);
          this.passwordData = {
            old_password: '',
            new_password: '',
            confirm_password: ''
          };
        } catch (err) {
          alert(err.response?.data?.error || "Password change failed.");
        }
      }
    }
  };
  </script>
  
  <style scoped>
  label, h1{
    font-family: "Concert One", serif;

  }
  .edit-profile-container {

    margin: auto;
    padding: 2rem;
    gap: 5vw;
  }
  input {
    display: block;
    width: 70%;
    margin-bottom: 1rem;
    border: 3px solid black !important; 
    background-color: white;
    font-size: 1.2vw;
    height: 5.5vh;
    padding: 10px;
    border-radius: 30px;
    color: black;
    
  }
  button {
    margin-right: 1rem;
  }
  h1{
    font-size: 4vw;
    text-align: center;
  }
  .edit {
    width: 40vw;
    height: 71vh;
    border: 4px solid black;
    flex-direction: column;
    border-radius: 30px;
    background-color: rgb(149, 194, 149);
    color: rgb(255, 255, 255);
      text-shadow: 2px 2px 0px #000000, -2px -2px 0px #8db161, 2px -2px 0px #8db161, -2px 2px 0px #8db161;

  }
  label{
    font-size: 1.5vw;
  }

  .edit button{
    width: 7vw;
    height: 6vh;
    border: 3px solid black;
    position: relative;
    top: 1vh;
    border-radius: 30px;
    font-size: 1.3vw;
    background-color: #8db161;
  }
  
  </style>
  