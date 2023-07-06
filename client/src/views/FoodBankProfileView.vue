<template>
    <div class="profile-container-food-bank container">
      <!-- Profile Dropdown -->
      <div class="profile-dropdown" v-if="associated_food_banks_ids.length > 1">
        <button class="btn dropdown-toggle" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
          {{ food_bank.name }}
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
          <li v-for="(food_bank, index) in associated_food_banks_data" :key="index">
            <a class="dropdown-item" @click="handleFoodBankSelection(index)">{{ food_bank.name }}</a>
          </li>
        </ul>
      </div>
  
      <!-- Title Section -->
      <div class="title-container d-flex justify-content-center flex-nowrap">
        <h1 class="p-title">{{ title }}</h1>
      </div>
  
      <!-- Form Section -->
      <div class="form-container d-flex justify-content-center flex-nowrap">
        <form class="row form-group form">
          <div class="row-md-6 form-group">
            <label for="name">Food Bank Name:</label>
            <input type="text" id="name" autocomplete="on" class="form-control" v-model="form.name" required>
          </div>
          <div class="row-md-6 form-group">
            <label for="address">Address:</label>
            <input type="text" id="address" autocomplete="on" class="form-control" v-model="form.address" required>
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


  
    <!-- Submission Section -->
    
  </template>
  

<script>
    export default {
        name: 'FoodBankProfileView',
        watch: {
            food_bank: {
                handler: function(newFoodBank){
                    this.title = 'Hello There ' + newFoodBank.name;
                    this.form.name = newFoodBank.name;
                    this.form.address = newFoodBank.address;
                    this.form.city = newFoodBank.city;
                    this.form.state = newFoodBank.state;
                    this.form.country = newFoodBank.country;
                    this.form.phone = newFoodBank.phone;
                },
                deep: true
            }
        },
        data() {
            return {
                form: {
                    name: '',
                    address: '',
                    city: '',
                    state: '',
                    country: '',
                    phone: ''
                },
                associated_food_banks_ids: [],
                associated_food_banks_data: [],
                food_bank: {},
                title: "Tell Us About Your Food Bank",

            }
        },
        mounted(){
            //get associated food bank IDs
            //get associated food bank data
            //get current food bank data
            this.fetchAssociatedFoodBanksIds();
        },

        methods:{
            //fetch associated foodbank ids
            fetchAssociatedFoodBanksIds(){
                this.axiosInstance.get('/food_bank/get_associated_food_banks_ids')
                    .then((response) => {
                        response = JSON.parse(response.data);
                        console.log(response)
                        this.associated_food_banks_ids = response
                        this.$toast.success('Successfully fetched food bank IDs');
                        console.log('associated food bank ids', this.associated_food_banks_ids.length);
                        if (this.associated_food_banks_ids.length > 0){
                            this.fetchAssociatedFoodBanksData();
                        }
                    })
                    .catch((error) => {
                        console.log("Error fetching associated food bank ids", error);
                        this.$toast.error('Error fetching food bank IDs');
                    });

            },

            //fetch associated foodbank data
            fetchAssociatedFoodBanksData(){
                this.axiosInstance.get('/food_bank/get_associated_food_banks_data', {
                    skipAuth: false,
                    params: {
                        current_food_bank: localStorage.getItem('current_food_bank')
                    }})
                    .then((response) => {
                        response = JSON.parse(response.data);
                        console.log(response)


                        for (let i = 0; i < this.associated_food_banks_ids.length; i++){
                            this.associated_food_banks_data[i] = response.associated_food_banks_data[i];
                        }
                        this.food_bank = response.current_food_bank_info;
                        this.form.name = this.food_bank.name;
                        this.form.address = this.food_bank.address;
                        this.form.city = this.food_bank.city;
                        this.form.state = this.food_bank.state;
                        this.form.country = this.food_bank.country;
                        this.form.phone = this.food_bank.phone;
                        this.title = this.food_bank.name
                        this.$toast.success('Successfully fetched food bank data');

                    })
                    .catch((error) => {
                        console.log("Error fetching associated food bank data", error);
                        this.$toast.error('Error fetching food bank data');
                    });

            },

            //user selected new food bank to manage via drop down (set current food bank id in sessions)
            handleFoodBankSelection(index) {;
                this.food_bank = this.associated_food_banks_data[index];
                localStorage.setItem('current_food_bank', this.associated_food_banks_data[index]._id);
            },

            onSubmit(event){
                event.preventDefault();

                //update current food bank data
                //send new data to db

                this.food_bank = {
                    name: this.form.name,
                    address: this.form.address,
                    city: this.form.city,
                    state: this.form.state,
                    country: this.form.country,
                    phone: this.form.phone
                }

                this.axiosInstance.post('/food_bank/add_food_bank',{selected: this.food_bank, skipAuth: false})
                    .then((response) => {
                        localStorage.setItem('current_food_bank', response.data.current_food_bank);
                        
                        window.location.reload();
                        this.$toast.success('Successfully added your food bank');
                        console.log('we added your food bank', this.food_bank);
                    })
                    .catch((error) => {
                        console.log(error);
                        this.$toast.error('Error adding food bank');
                    });

            },
        }


    }
</script>

<style scoped>
    
</style>