<template>
  <div class="profile-container container">
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
    <div class="form-container d-flex justify-content-center flex-nowrap">

      <form class="row form ">
        <div class="row-md-6 form-group">
          <label for="name">Business Name:</label>
          <input type="text" id="name" class="form-control" v-model="name">
        </div>

        <div class="row-md-6 form-group">
          <label for="address">Business Address:</label>
          <input type="text" id="address" class="form-control" v-model="address">
        </div>
        <div class="w-100"></div>

        <div class="row-md-6 form-group">
          <label for="city">City:</label>
          <input type="text" id="city" class="form-control" v-model="city">
        </div>
        <div class="w-100"></div>
        <div class="row form-group">
          <div class="col-md-6 form-group">
            <label for="state">State:</label>
            <input type="text" id="state" class="form-control" v-model="state">
          </div>

          <div class="col-md-6 form-group">
            <label for="country">Country:</label>
            <input type="text" id="country" class="form-control" v-model="country">
          </div>
        </div>
        <div class="row-md-6 form-group">
            <label for="number">Phone Number:</label>
            <input type="text" id="phone" class="form-control" v-model="phone">
        </div>
        <div class="col-md-12 d-flex justify-content-center">
          <div class="submit-button">
            <input type="button" @click="onSubmit" id="submitButton" class="btn btn-primary form-button" value="Submit"/>
          </div>
        </div>
      </form>  
    </div>
  </div>
  <div class="submission container">
    <div id="profile-results" class="profile-results card-deck container d-flex flex-row align-items-center ">
      <div class="card" v-for="(key, index) in Object.keys(yelp_response).slice(0, 3)" :key="index">
        <img :src="yelp_response[key].image" class="card-img-top" alt="Restaurant Image">
        <div class="card-body d-flex flex-column" @click="restaurantSelect(index)">
          <h5 class="card-title">{{ yelp_response[key].name }}</h5>
          <p class="card-text">{{ yelp_response[key].address }}</p>
          <p class="card-text">Phone: {{ yelp_response[key].phone }}</p>
          <p class="card-text">Rating: {{ yelp_response[key].rating }}</p>
          <div class="mt-auto">
            <a :href="yelp_response[key].url" target="_blank" class="btn btn-primary button" style="background: #4f61ff">View on Yelp</a>
          </div>
        </div>
      </div>
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
      yelp_response: {},
      submitted: false
    };
  },
  methods: { 
        onSubmit(event) {
          event.preventDefault();
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
          axios.post('/api/get_restaurants', data).then((response) => {
            const responseData = JSON.parse(response.data.message).businesses
            const amount = responseData.length
            if (amount > 0) {
              this.$toast.success("Success!");
            }
            for (let i = 0; i < amount; i++){
              this.yelp_response[i] = {
                name: responseData[i].name,
                address: responseData[i].location.display_address.join(', '),
                phone: responseData[i].display_phone,
                rating: responseData[i].rating,
                image: responseData[i].image_url,
                url: responseData[i].url,
                price: responseData[i].price,
                categories: responseData[i].categories,
                distance: responseData[i].distance,
                coordinates: responseData[i].coordinates
              }
            }
            this.submitted = true


          }).catch((error) => {
            console.log(error)
            this.$toast.error("Error! Please provide accurate information")
          })
        },
        restaurantSelect(index){
          axios.post("/api/set_restaurant", {"selected": this.yelp_response[index], "current_user": localStorage.getItem('email')}).then((response) => {
            console.log("set restaurant", this.yelp_response[index])
            this.$toast.success("Success!");
          }).catch((error) => {
            this.$toast.error("Error selecting restaurant")
          })
        }
  }

};
</script>


