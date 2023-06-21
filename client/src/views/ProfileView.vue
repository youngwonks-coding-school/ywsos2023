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
    <div class="form-container d-flex justify-content-center flex-nowrap">

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
          <input type="text" id="number" class="form-control" v-model="number">
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
      </form>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: '',
      address: '',
      number: '',
      city: '',
      state: '',
      country: ''
    };
  }
};
</script>
