
<template>
  <div class="container-fluid dash-container">
    <div class=" dashboard-content">
      <div class="col-md-5 mb-3">
        <h2 class="d-title"> Dashboard </h2>
      </div>
      <div class="container-fluid pt-5 dashboard">
        <div class="container-fluid row panel-container ">
          <div class="col-md-6 p-4 container-fluid overflow-auto food-content" ref="foodContainer">
            
            
            <div v-for="(food, index) in foods" :key="index" class="food-row-wrapper">
              <div class="row food-row p-2" @click="editFoodRow(index,true,false)" :class="{ 'fade-out': food.isDeleted, 'editing': food.isEditing }">
                
                <div v-if="food.unSaved" class="col-lg-1 row-item">
                  <v-icon class="unsaved" name="bi-exclamation-circle-fill" scale="1" @mouseover="showTooltip[index][0] = true" @mouseleave="showTooltip[index][0] = false" />
                  <div class="tooltip" v-if="showTooltip[index][0]">Unsaved Changes</div>
                </div>

                <div class="col-lg-3 row-item">
                  <input type="text" class="food-item-name" placeholder="Food" v-model="food.name" @click="editFoodRow(index, true, false)" @input="editFoodRow(index, true)" />
                </div>

                <div class="col-lg-3 row-item">
                  <div class="input-group">
                    <input class="form-control food-item-quantity" placeholder="Quantity" type="number" min="0" step="1" v-model="food.quantity" @click="editFoodRow(index, true, false)"  @input="editFoodRow(index, true)"/>
                    <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false" @click="editFoodRow(index, true, false)" >{{ food.unit }}</button>
                    <div class="dropdown-menu dropdown-menu-end">
                      <a class="dropdown-item" href="#" v-for="option in unitOptions" :key="option" @click="food.unit = option; editFoodRow(index, true)">{{ option }}</a>
                    </div>
                  </div>
                </div>

                <div class="col-lg-3 row-item">
                  <input type="date" class="form-control food-item-expire" v-model="food.expireDate" @mouseover="showTooltip[index][1] = true" @mouseleave="showTooltip[index][1] = false" @click="editFoodRow(index, true, false)" @input="editFoodRow(index, true)" />
                  <div class="tooltip" v-if="showTooltip[index][1]">Expiration Date</div>
                </div>

                <div class="col-lg-1 row-item">

                  <div class="food-item-save-edit">
                    <v-icon class="food-item-edit" v-if="!food.isEditing" @click="editFoodRow(index, true, false); showTooltip[index][2] = false" name="bi-pencil-square" scale="1.5" @mouseover="showTooltip[index][2] = true" @mouseleave="showTooltip[index][2] = false" />
                    <v-icon v-if="food.isEditing" @click="saveFoodRow(index, food.name, food.quantity, food.unit, food.expireDate); showTooltip[index][3] = false" name="ri-save-3-line" scale="1.5" @mouseover="showTooltip[index][3] = true" @mouseleave="showTooltip[index][3] = false" />
                  </div>
                  <div class="tooltip" v-if="showTooltip[index][2] && !food.isEditing">Edit Row</div>
                  <div class="tooltip" v-if="showTooltip[index][3] && food.isEditing">Save Row</div>
                
                </div>

                <div class="col-lg-1 row-item">
                  <span class="food-item-trash">
                    <v-icon @click="removeFoodRow(index)" name="bi-trash" scale="1.5" />
                  </span>
                </div>
              </div>
            </div>
            <div class="container">
              <button @click="addFoodRow" class="btn btn-primary food-item-add mt-3"><v-icon class="food-item-add-icon" name="io-add-circle-sharp" scale="1.4"/></button>
            </div>
          </div>


          <div class="col-md-6 container-fluid overflow-auto info-container">
            <div class="row container info-content">
              <div class="col-md-5 container-fluid info-panel">
                <h2 class="current-orders-title">Current Orders</h2>
                <h2 class="current-orders-title">5</h2>
              </div>
              <div class="col-md-5 container-fluid info-panel">
                <h2 class="current-orders-title">Notifications</h2>
                <h2 class="current-orders-title">5</h2>
              </div> 
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Popper from "vue3-popper";
import { v4 as uuidv4 } from 'uuid';

export default {
  components: {
      Popper,
  },
  data() {
    return {
      email: '',
      password: '',
      unitOptions: ["qty", "lbs", "oz", "g", "kg", "L", "mL"],
      foods: [],
      
      //bootstrap tooltips not working **custom tooltips**
      //p1: unsaved changes, p2: expiration date, p3: save/edit
      showTooltip: [[false, false, false, false]],
    }
  },
  mounted() {
    this.verifyUserSession()
    const uuid = uuidv4();

    this.axiosInstance
      .post(
        '/restaurant/get_food_data',
        {
          current_restaurant_id: localStorage.getItem('current_restaurant'),
          skipAuth: false
        })
      .then((response) => {
        this.showTooltip = new Array(response.data.food_data.length).fill([false, false, false, false])

        console.log(response.data.food_data)
        if (response.data.food_data.length > 0){
          this.foods = response.data.food_data.map((food) => {
          return {
            name: food.name,
            quantity: food.quantity,
            unit: food.unit,
            expireDate: food.expire_date,
            isDeleted: false,
            isEditing: false,
            unSaved: false,
            _id: food._id
          }
        })
        }
      })
      .catch((error) => {
        console.log(error)
      })

    // this.foods.push({
    //   name: "Potatoes",
    //   amount: 5,
    //   unit: "qty",
    //   expireData: "2023-07-31",
    //   isDeleted: false,
    //   isEditing: false,
    //   unSaved: false,
    //   _id: uuid.toString()
    // });

  },
  methods: {


    editFoodRow(index, isEditing, madeChanges = true) {
      for (let i = 0; i < this.foods.length; i++) {
        this.foods[i].isEditing = false
      }

      this.foods[index].isEditing = isEditing

      //user may have clicked on the edit button or on row but may have not changed anything
      //user hasnt made changes to row -> and row is not already unsaved -> set unsaved to false
      if (!madeChanges && !this.foods[index].unSaved){
        this.foods[index].unSaved = false
      } else{
        this.foods[index].unSaved = madeChanges
      }
    },

    addFoodRow() {
      const uuid = uuidv4();
      this.foods.push({name: "Potatoes", amount: 5, unit: "qty", expireData:"2023-07-31", isDeleted: false, isEditing: true, unSaved: false, _id: uuid})
      this.editFoodRow(this.foods.length-1, true, false)

      //add new tooltip for new row
      this.showTooltip.push([false, false, false, false])

      //scroll to the bottom of the food container
      this.$nextTick(() => {
        const foodContainer = this.$refs.foodContainer;
        if (foodContainer) {
          foodContainer.lastChild.scrollIntoView({
            behavior: "smooth",
            block: "end"
          });
        }
      });
    },
    async removeFoodRow(index) {
      this.foods[index].isDeleted = true;
      this.showTooltip.splice(index, 1);

      await this.axiosInstance
        .post(
          '/restaurant/delete_food',
          {
            current_restaurant_id: localStorage.getItem('current_restaurant'),
            skipAuth: false,
            _id: this.foods[index]._id
          }
        )
        .then((response) => {
          console.log(response.data)
          this.$toast.success("Food Item Deleted")
        })
        .catch((error) => {
          console.log(error)
          this.$toast.success("Error Deleting Food Item")
        })

      // Wait for fade animation to complete
      setTimeout(() => {
        this.foods.splice(index, 1);
      }, 500);

    },


    async saveFoodRow(index, name, quantity, unit, expireDate) {
      try {
        this.foods[index].isEditing = !this.foods[index].isEditing;
        this.foods[index].unSaved = false;

        this.foods[index].name = name;
        this.foods[index].amount = quantity;
        this.foods[index].unit = unit;
        this.foods[index].expireDate = expireDate;

        console.log(this.foods[index]._id)
        const response = await this.axiosInstance.post('/restaurant/add_food', {
          current_restaurant_id: localStorage.getItem('current_restaurant'),
          skipAuth: false,
          food_data: {
            name: this.foods[index].name,
            amount: this.foods[index].amount,
            unit: this.foods[index].unit,
            expireDate: this.foods[index].expireData,
          },
          _id: this.foods[index]._id,
        });

        console.log(response.data);
        this.$toast.success('Food Item Saved');
      } catch (error) {
        console.log(error);
        this.$toast.error(error.response.data.msg);
      }
    },


    verifyUserSession() {
      this.axiosInstance
        .post(
          '/api/auth/verify',
          {},
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('accessToken')}`
            }
          }
        )
        .then((response) => {
          console.log(response.data.message)
          this.$toast.success('Already Logged in.')
        })
        .catch((error) => {
          console.log(error)
          this.$toast.error(error.response.data.msg)
          this.axiosInstance
            .post(
              '/api/auth/refresh',
              {},
              {
                headers: {
                  Authorization: `Bearer ${localStorage.getItem('refreshToken')}`
                }
              }
            )
            .then((response) => {
              console.log(response.data.message)
              this.$toast.success(response.data.message)
              localStorage.setItem('accessToken', response.data.access_token)
            })
            .catch((error) => {
              console.log(error)
              localStorage.removeItem('refreshToken')
              localStorage.removeItem('accessToken')
              this.$router.push('/login')

              this.$toast.error(error.response.data.msg)
            })
        })
    }
  },
  computed: {
    isValidEmail() {
      const emailRegex = /^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$/
      return emailRegex.test(this.email)
    },
    isValidPassword() {
      return this.password.length >= 8
    }
  }
}
</script>
