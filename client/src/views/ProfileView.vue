<template>
  <div class="profile-container container">
    <div class="title-container d-flex justify-content-center flex-nowrap">
      <h1 class="p-title">{{this.title}}</h1>
      <div v-if="associated_restaurants_ids.length > 1">

      </div>
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
          <input type="text" id="name" class="form-control" v-model="form.name">
        </div>

        <div class="row-md-6 form-group">
          <label for="address">Business Address:</label>
          <input type="text" id="address" class="form-control" v-model="form.address">
        </div>
        <div class="w-100"></div>

        <div class="row-md-6 form-group">
          <label for="city">City:</label>
          <input type="text" id="city" class="form-control" v-model="form.city">
        </div>
        <div class="w-100"></div>
        <div class="row form-group">
          <div class="col-md-6 form-group">
            <label for="state">State:</label>
            <input type="text" id="state" class="form-control" v-model="form.state">
          </div>

          <div class="col-md-6 form-group">
            <label for="country">Country:</label>
            <input type="text" id="country" class="form-control" v-model="form.country">
          </div>
        </div>
        <div class="row-md-6 form-group">
            <label for="number">Phone Number:</label>
            <input type="text" id="phone" class="form-control" v-model="form.phone">
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
      //form restaurant data that user entered
      form:{name: '', address: '', phone: '', city: '', state: '', country: '', type: ''},


      yelp_response: {},
      restaurant: {},
      associated_restaurants_ids: [],
      associated_restaurants: {},
      selectedRestaurant: null,


      email: '',
      title: 'Let\'s Figure Out Who You Are!',
      submitted: false
    };
  },
  mounted() {
    //get the current user email and all sessions
    axios.get('/api/auth/get_sessions_for_user', {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('accessToken')}`
      }
    })
    .then((response) => {
      this.email = response.data.email
      console.log("Found User Session + Email " + this.email)

      //get all restaurants associated with user (id)
      this.associated_restaurants_ids = response.data.associated_restaurants_ids

      //check user has set up restaurant
      console.log(this.associated_restaurants_ids.length)
      if (this.associated_restaurants_ids.length != undefined && this.associated_restaurants_ids.length > 0){
        //check user is associated with more than one restaurants (allow for managing)
        axios.get(`/api/profile/previous_restaurant?current_user=${this.email}`)
          .then(response => {
            response = JSON.parse(response.data)
            //give all associated_restaurants to all_user_restaurants
            for (let i = 0; i < response.associated_restaurants.length; i++){
              this.associated_restaurants[i] = response.associated_restaurants[i]
            }
            //give current restaurant info to restaurant
            this.restaurant = response.current_restaurant_info;
            
            this.form.name = this.restaurant.name; this.form.address = this.restaurant.address; this.form.phone = this.restaurant.phone; this.form.city = this.restaurant.city; this.form.state = this.restaurant.state; this.form.country = this.restaurant.country; this.form.type = this.restaurant.type;
            this.title = 'Hello There ' + this.restaurant.name 
          }).catch(error => {console.error(error);});
      }
    }).catch((error) => {console.log(error)});


  },
  methods: { 
        onSubmit(event) {
          event.preventDefault();
          this.form.name = document.getElementById('name').value;
          this.form.address = document.getElementById('address').value;
          this.form.phone = document.getElementById('phone').value;
          this.form.city = document.getElementById('city').value;
          this.form.state = document.getElementById('state').value;
          this.form.country = document.getElementById('country').value;
          this.form.type = document.getElementById('toggle').checked ? 'restaurant' : 'food';
          console.log("submitted")
          this.profile_data();

        },
        profile_data(){
          const data = {
            name: this.form.name,
            address: this.form.address,
            phone: this.form.phone,
            city: this.form.city,
            state: this.form.state,
            country: this.form.country,
            type: this.form.type,
          }
          //get possible restaurants from yelp based on entered form data
          axios.post('/api/profile/get_restaurants', data).then((response) => {
            const responseData = JSON.parse(response.data.message).businesses
            const amount = responseData.length
            if (amount > 0) {
              this.$toast.success("Success!");
            }
            for (let i = 0; i < amount; i++){
              //insert all results into yelp_response (will be accessed to turn data into cards to select)
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
          //user selected restaurant -> server will send this data to db

          axios.post("/api/profile/add_restaurant", {"selected": this.yelp_response[index], "current_user": this.email}).then(() => {
            this.restaurant = {name: this.yelp_response[index].name, address: this.yelp_response[index].address, phone: this.yelp_response[index].phone, rating: this.yelp_response[index].rating, image: this.yelp_response[index].image, url: this.yelp_response[index].url, price: this.yelp_response[index].price,categories: this.yelp_response[index].categories,distance: this.yelp_response[index].distance,coordinates: this.yelp_response[index].coordinates}
            console.log("we set your restaurant", this.restaurant)
            window.location.reload()
          }).catch((error) => {
            console.log(error)
            this.$toast.error("Error selecting restaurant")
          })
        }
  }

};
</script>


