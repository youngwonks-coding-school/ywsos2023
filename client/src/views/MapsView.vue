<template>
  <div class="container card col-12 col-sm-10 col-md-8 col-lg-6">
    <div class="card-body">
      <h5 class="card-title text-center mb-4">Maps</h5>
      <form @submit.prevent="onCreatePost">
        <div class="input-group mb-3">
          <select class="form-select" v-model="placeType">
            <option value="null">Please select an option</option>
            <option value="restaurant">I am looking for restaurants</option>
            <option value="food_bank">I am looking for food banks</option>
          </select>
          <button class="btn btn-primary" type="submit">Search</button>
        </div>
      </form>
    </div>
    <GMapMap :center="currPos" :zoom="12" map-type-id="terrain" style="width: 100%; height: 450px">

      <GMapMarker v-if="currPos" :position="currPos" icon="http://maps.google.com/mapfiles/ms/icons/blue-dot.png">
      </GMapMarker>
      <GMapMarker :key="m.id" v-for="(m, index) in myMarkers" :position="m.myPosition" :clickable="true" :draggable="true"
        icon="http://maps.google.com/mapfiles/ms/icons/red-dot.png" @click="datacollect(m), openMarker(m.id, m)">
        <GMapInfoWindow :closeclick="true" @closeclick="openMarker(null)" :opened="openedMarkerID === m.id">
          <div>
            <p>Name: {{ infowindowData.name }}</p>
            <p>Address: {{ infowindowData.vicinity }}</p>
            <p>Rating: {{ infowindowData.rating }}/5</p>
          </div>
        </GMapInfoWindow>
      </GMapMarker>

    </GMapMap>


  </div>
</template>
  
<script>
import { computed, ref } from 'vue'
import axios from 'axios'
import { useGeolocation } from '@/useGeolocation.js'


export default {
  name: 'App',

  data() {
    const myMarkers = ref([]); // Define myMarkers as a reactive ref
    let myResults = {}
    const infowindowData = ref({ name: '', vicinity:'', rating: '' });


    return { placeType: null, myMarkers, myResults, openedMarkerID: null, infowindowData }
  },

  setup() {






    const { coords } = useGeolocation()
    const currPos = computed(() => ({
      lat: coords.value.latitude,
      lng: coords.value.longitude
    }))





    return { currPos }
  },

  methods: {

    onCreatePost() {
      this.myMarkers = [];



      // Define the parameters to be sent to the server
      const baseUrl = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json';
      const radius = 5000;
      const type = "food";
      const keyword = this.placeType;
      // Get the location
      const location = {
        lat: this.currPos.lat,
        lng: this.currPos.lng,
      };

      // Send the parameters to the server
      const apiUrl = '/api/maps/fetch_places';
      const requestData = {
        baseUrl: baseUrl,
        radius: radius,
        type: type,
        keyword: keyword,
        location: location,

      };

      axios.post(apiUrl, requestData)
        .then(response => {
          // Handle the server response with JSON data if needed
          let myResultsData = JSON.parse(response.data)
          let myMarkers = this.myMarkers
          let i = 0
          while (myResultsData.results[i]) {
            const myLocation = myResultsData.results[i]
            const myMarker = {
              myPosition: {
                lat: myLocation.geometry.location.lat,
                lng: myLocation.geometry.location.lng
              },
              id: i,
              index: i
            }
            myMarkers.push(myMarker)
            i++
          }
          this.myResults = myResultsData;



        })
        .catch(error => {
          // Handle any errors
          console.error(error);
        });
      return { myResults }
    },

    datacollect(m) {
      this.infowindowData.name = this.myResults.results[m.index].name;
      this.infowindowData.vicinity = this.myResults.results[m.index].vicinity;
      this.infowindowData.rating = this.myResults.results[m.index].rating;


    },
    openMarker(id, m) {
      this.openedMarkerID = id
    }








  }

}
</script>
