<template>
  <div class="container mt-5 mb-5">
    <div class="title-container d-flex justify-content-center flex-nowrap">
      <h1 class="p-title">Let's Figure Out Who You Are!</h1>
    </div>
    <div class="toggle-button">
        <input type="checkbox" id="toggle" class="toggle-input">
        <label for="toggle" class="toggle-label">
          <span class="toggle-text mr-4">Restaurant</span>
          <span class="toggle-switch"></span>
          <span class="toggle-text ml-4">Food</span>
        </label>
      </div>
    <div class="form-container d-flex justify-content-center flex-nowrap" v-on:submit.prevent="onSubmit">

      <form class="row form">
        <div class="col-md-6 form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" class="form-control" v-model="name">
        </div>

        <div class="col-md-6 form-group">
          <label for="address">Address:</label>
          <input type="text" id="address" class="form-control" v-model="address">
        </div>
        <div class="w-100"></div>
        <div class="col-md-6 form-group">
          <label for="number">Phone Number:</label>
          <input type="text" id="phone" class="form-control" v-model="phone">
        </div>

        <div class="col-md-6 form-group">
          <label for="city">City:</label>
          <input type="text" id="city" class="form-control" v-model="city">
        </div>
        <div class="w-100"></div>
        <div class="col-md-6 form-group">
          <label for="state">State:</label>
          <input type="text" id="state" class="form-control" v-model="state">
        </div>

        <div class="col-md-6 form-group">
          <label for="country">Country:</label>
          <input type="text" id="country" class="form-control" v-model="country">
        </div>
        <div class="col-md-12 d-flex justify-content-center">
          <div class="submit-button">
            <input type="submit" @click="onSubmit()" class="btn btn-primary button" value="Submit"/>
          </div>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      name: '',
      address: '',
      phone: '',
      city: '',
      state: '',
      country: '',
      yelp_response: '',
    };
  },
  methods: { 
        onSubmit() {
          this.name = document.getElementById('name').value;
          this.address = document.getElementById('address').value;
          this.phone = document.getElementById('phone').value;
          this.city = document.getElementById('city').value;
          this.state = document.getElementById('state').value;
          this.country = document.getElementById('country').value;
          this.type = document.getElementById('toggle').checked ? 'restaurant' : 'food';
          console.log("submitted")
          this.profile_data();

        },
        profile_data(){
          const data = {
            name: this.name,
            address: this.address,
            phone: this.phone,
            city: this.city,
            state: this.state,
            country: this.country,
            type: this.type
          }
          axios.post('/api/auth/profile_data', data).then((response) => {
            const responseData = JSON.parse(JSON.stringify(response.data.message))
            console.log('buisness count' + responseData[0])
            this.yelp_response = responseData
          }).catch((error) => {
            console.log(error)
          })
        }
    }

};
</script>


