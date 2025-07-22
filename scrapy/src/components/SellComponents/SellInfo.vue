<template>
  <div class="container">
    <h1 class="mainHeading">SHARE YOUR OFFER</h1>

    <form @submit.prevent="submitPost" enctype="multipart/form-data">
      <div class="category flex">
        <h1>CATEGORY</h1>
        <h1 style="color: black; font-size: 5vw;">{{ category }}</h1>
      </div>

      <div class="info flex">
        <label for="title">TITLE</label>
        <input type="text" id="title" v-model="title" required style="border: 1px solid black;"/>

        <label for="desc">DESCRIPTION</label>
        <textarea id="desc" v-model="description" required></textarea>

        <label for="price">PRICE</label>
        <input type="number" id="price" v-model="price" required style="border: 1px solid black;"/>
      </div>

      <div class="condition flex">
        <h1>CONDITION</h1>
        <div class="level flex">
          <label><input type="radio" name="condition" value="Excellent" v-model="condition" required /> Excellent</label>
          <label><input type="radio" name="condition" value="Good" v-model="condition" /> Good</label>
          <label><input type="radio" name="condition" value="Fair" v-model="condition" /> Fair</label>
          <label><input type="radio" name="condition" value="Poor" v-model="condition" /> Poor</label>
          <label><input type="radio" name="condition" value="Broken" v-model="condition" /> Broken</label>
        </div>
      </div>

      <div class="contact flex">
        <h1>CONTACT</h1>
        <div class="cont-type flex">
          <label><input type="radio" name="contact" value="Chat and Call" v-model="contact" required /> Chat and Call</label>
          <label><input type="radio" name="contact" value="Chat Only" v-model="contact" /> Chat Only</label>
          <label><input type="radio" name="contact" value="Call Only" v-model="contact" /> Call Only</label>
        </div>
      </div>

      <div class="delivery flex">
        <h1>DELIVERY</h1>
        <div class="preference flex">
          <label><input type="radio" name="delivery" value="Pickup Only" v-model="delivery" required /> Pickup Only</label>
          <label><input type="radio" name="delivery" value="Willing to Ship" v-model="delivery" /> Willing to Ship</label>
        </div>
      </div>

      <!-- Multiple Image Upload -->
      <div class="image-upload flex items-center gap-4">
        <h1>UPLOAD IMAGES</h1>

        <input
          type="file"
          id="file-upload"
          multiple
          @change="handleImageUpload"
          accept="image/*"
          style="display: none"
        />

        <label for="file-upload" class="cursor-pointer">
          <img width="50" height="50" src="https://img.icons8.com/ios/50/image--v1.png" alt="upload" />
        </label>

        <!-- Preview thumbnails -->
        <div class="preview-images">
          <div v-for="(img, index) in imageFiles" :key="index" class="preview-box">
            <img :src="img.preview" class="preview-thumb" />
            <button @click="removeImage(index)" class="remove-btn">x</button>
          </div>
        </div>
      </div>

      <button class="submit flex" type="submit">POST</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'SellInfo',
  props: {
    category: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      title: '',
      description: '',
      price: '',
      condition: '',
      contact: '',
      delivery: '',
      imageFiles: [] // array of { file, preview }
    };
  },
  methods: {
    handleImageUpload(event) {
      const selected = Array.from(event.target.files);
      for (const file of selected) {
        if (this.imageFiles.length >= 5) {
          alert("You can upload up to 5 images only.");
          break;
        }
        const preview = URL.createObjectURL(file);
        this.imageFiles.push({ file, preview });
      }
      event.target.value = null;
    },

    removeImage(index) {
      this.imageFiles.splice(index, 1);
    },

    async submitPost() {
      if (this.imageFiles.length === 0) {
        alert("Please upload at least one image.");
        return;
      }

      const formData = new FormData();
      formData.append('category', this.category);
      formData.append('title', this.title);
      formData.append('description', this.description);
      formData.append('price', this.price);
      formData.append('condition', this.condition);
      formData.append('contact', this.contact);
      formData.append('delivery', this.delivery);

      this.imageFiles.forEach(imgObj => {
        formData.append('attachments', imgObj.file); // MUST MATCH backend
      });

      try {
        const token = localStorage.getItem('user.access');
        const response = await axios.post('http://localhost:8000/api/scrap-posts/scrapposts/', formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          }
        });

        alert('Post created successfully!');
        this.$router.push('/mainpage');
      } catch (error) {
        alert('Error posting scrap: ' + (error.response?.data?.detail || error.message));
      }
    }
  }
};
</script>

<style scoped>
.mainHeading {
  color: rgb(0, 0, 0);
  font-size: 4vw;
  font-family: 'Concert One', serif;
  text-align: center;
}
input {
  width: 25vw;
  height: 7vh;
  font-size: 1.2vw;
}
input[type='radio'] {
  width: 1vw;
  display: block;
  margin: 0 auto;
}
textarea {
  resize: none;
  border: 1px solid black;
  outline: none;
  width: 40vw;
  height: 25vh;
  border-radius: 20px;
  padding: 20px;
  font-size: 1.2vw;
}
#price {
  width: 8vw;
  height: 5vh;
}
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.container h1 {
  color: lightgreen;
  font-size: 6vw;
  font-family: 'Concert One', serif;
}
.container {
  width: 60vw;
  min-height: 100vh;
  margin: 10vh auto;
  border-radius: 30px;
  box-shadow: 0 0 20px rgb(233, 233, 233);
}
.category {
  gap: 5vw;
}
.info {
  flex-direction: column;
  position: relative;
  top: 5vh;
  gap: 2vh;
}
.info label {
  font-size: 4vw;
  font-family: 'Concert One', serif;
}
.condition,
.delivery,
.contact {
  flex-direction: column;
  position: relative;
  top: 10vh;
}
.condition h1,
.delivery h1,
.contact h1 {
  font-size: 4vw;
}
.level label,
.cont-type label,
.preference label,
.delivery label {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 1.2vw;
  margin: 1vh;
}
.submit {
  width: 8vw;
  height: 6vh;
  color: white;
  background-color: lightgreen;
  border-radius: 30px;
  border: 3px solid black;
  font-size: 1.9vw;
  margin: 15vh auto;
  font-family: 'Concert One', serif;
  cursor: pointer;
  position: relative;
  bottom: 5vh;
}
.image-upload {
  margin-top: 10vh;
  font-size: 1.5vw;
  flex-direction: column;
}
.preview-images {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}
.preview-box {
  position: relative;
}
.preview-thumb {
  width: 10vw;
  height: 20vh;
  object-fit: cover;
  border-radius: 10px;
  box-shadow: 0 0 5px #aaa;
}
.remove-btn {
  position: absolute;
  top: -8px;
  right: -8px;
  background: red;
  color: white;
  border: none;
  border-radius: 50%;
  width: 30px;
  height: 36px;
  cursor: pointer;
  font-weight: bold;
}
</style>
