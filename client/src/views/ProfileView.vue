<template>
  <div class="profile-container container">
    <div class="profile-dropdown" v-if="associated_restaurants_ids.length > 1">
      <button class="btn dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
        {{ restaurant.name }}
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
        <li v-for="(restaurant, index) in associated_restaurants" :key="index">
          <a class="dropdown-item" @click="handleRestaurantSelection(index)">{{ restaurant.name }}</a>
        </li>
      </ul>
    </div>
    <div class="title-container d-flex justify-content-center flex-nowrap">
      <h1 class="p-title">{{this.title}}</h1>
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
import { reactive, toRefs } from 'vue';

const axiosInstance = axios.create({
  baseURL: 'http://127.0.0.1:4000/api', // Assuming the base URL is '/api'
});

export default {
  watch: {
    restaurant: {
      handler: function(newRestaurant) {
        this.title = 'Hello There ' + newRestaurant.name;
        this.form.name = newRestaurant.name;
        this.form.address = newRestaurant.address;
        this.form.phone = newRestaurant.phone;
        this.form.city = newRestaurant.city;
        this.form.state = newRestaurant.state;
        this.form.country = newRestaurant.country;
        this.form.type = newRestaurant.type;
      },
      deep: true
    }
  },
  data() {
    return {
      form: {
        name: '',
        address: '',
        phone: '',
        city: '',
        state: '',
        country: '',
        type: ''
      },
      yelp_response: {},
      restaurant: {},
      associated_restaurants_ids: [],
      associated_restaurants: {},
      current_restaurant_index: 0,
      email: '',
      title: "Tell Us About Your Business",
      submitted: false
    };
  },
  mounted() {
    // Request interceptor
    axiosInstance.interceptors.request.use(
      (config) => {
        const accessToken = localStorage.getItem('accessToken');
        if (!config.skipAuth){

          config.headers.Authorization = `Bearer ${accessToken}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    axiosInstance.interceptors.response.use(
      (response) => {
        return response;
      },
      async (error) => {
        if (error.response.status === 401) {
          try {
            const refreshResponse = await axiosInstance.post('/auth/refresh', {
              Authorization: `Bearer ${localStorage.getItem('refreshToken')}`
            });
            localStorage.setItem('accessToken', refreshResponse.data.accessToken);
            return axiosInstance(error.response.config);
          } catch (error) {
            $toast.error('Axios Instance \n Refresh token error');
            console.log('Axios Instance \n Refresh token error:', error)
            return Promise.reject(error);
          }
        }
        return Promise.reject(error);
      }
    );

    axiosInstance
      .get('/auth/get_sessions_for_user', {skipAuth: false})
      .then((response) => {
        this.email = response.data.email;
        this.associated_restaurants_ids = response.data.associated_restaurants_ids;

        this.$toast.success("Successfully retrieved user info")
        console.log("Successfully retrieved " + this.email + "info -> associated restaurants: " + this.associated_restaurants_ids.length);

        //user has previously set up restaurant -> we need to access that information
        if (this.associated_restaurants_ids.length > 0) {
            axiosInstance
            .get('/profile/previous_restaurant', {
              skipAuth: false,
              params: {
                current_restaurant: localStorage.getItem('current_restaurant')
              },
            })
            .then((response) => {
              response = JSON.parse(response.data);
              //Get data for each restaurant under user
              for (let i = 0; i < this.associated_restaurants_ids.length; i++) {
                this.associated_restaurants[i] = response.associated_restaurants[i];
              }
              // Get data for current restaurant under user
              this.restaurant = response.current_restaurant_info;

              this.form.name = this.restaurant.name;
              this.form.address = this.restaurant.address;
              this.form.phone = this.restaurant.phone;
              this.form.city = this.restaurant.city;
              this.form.state = this.restaurant.state;
              this.form.country = this.restaurant.country;
              this.form.type = this.restaurant.type;
              this.title = 'Hello There ' + this.restaurant.name;
            })
            .catch((error) => {
              this.$toast.error("Error finding previous restaurants")
              console.log("Error finding previous restaurants: ", error )
            });
        }
      })
      .catch((error) => {
        this.$toast.error("Error finding previous restaurants")
        console.log("Error finding previous restaurants: ", error )
      });
  },
  methods: {
    //user selected new restaurant to manage via drop down (set current restaurant id in sessions)
    handleRestaurantSelection(index) {;
      this.restaurant = this.associated_restaurants[index];
      localStorage.setItem('current_restaurant', this.associated_restaurants[index]._id);
    },
    onSubmit(event) {
      event.preventDefault();
      this.form.name = document.getElementById('name').value;
      this.form.address = document.getElementById('address').value;
      this.form.phone = document.getElementById('phone').value;
      this.form.city = document.getElementById('city').value;
      this.form.state = document.getElementById('state').value;
      this.form.country = document.getElementById('country').value;
      this.form.type = document.getElementById('toggle').checked ? 'restaurant' : 'food';
      console.log('submitted');
      this.profile_data();
    },
    profile_data() {
      const data = {
        name: this.form.name,
        address: this.form.address,
        phone: this.form.phone,
        city: this.form.city,
        state: this.form.state,
        country: this.form.country,
        type: this.form.type
      };
      // Get possible restaurants from Yelp based on entered form data
      axiosInstance
        .post('/profile/get_restaurants', {'data': data, skipAuth: false})
        .then((response) => {
          const responseData = JSON.parse(response.data.message).businesses;
          const amount = responseData.length;
          if (amount > 0) {
            this.$toast.success(amount + ' restaurants found!');
          }
          for (let i = 0; i < amount; i++) {
            // Insert all results into yelp_response (will be accessed to turn data into cards to select)
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
            };
          }
          this.submitted = true;
        })
        .catch((error) => {
          console.log(error);
          this.$toast.error('Error! Getting Restaurants');
        });
    },
    restaurantSelect(index) {
      // User selected restaurant -> server will send this data to the database
      axiosInstance
        .post('/profile/add_restaurant', { selected: this.yelp_response[index]})
        .then((response) => {
          localStorage.setItem('current_restaurant', response.data.current_restaurant)
          this.restaurant = {
            name: this.yelp_response[index].name,
            address: this.yelp_response[index].address,
            phone: this.yelp_response[index].phone,
            rating: this.yelp_response[index].rating,
            image: this.yelp_response[index].image,
            url: this.yelp_response[index].url,
            price: this.yelp_response[index].price,
            categories: this.yelp_response[index].categories,
            distance: this.yelp_response[index].distance,
            coordinates: this.yelp_response[index].coordinates
          };
          this.$toast.success('Successfully set your restaurant');
          console.log('we set your restaurant', this.restaurant);
          window.location.reload();
        })
        .catch((error) => {
          console.log(error);
          this.$toast.error('Error selecting restaurant');
        });
    }
  }
};
</script>



