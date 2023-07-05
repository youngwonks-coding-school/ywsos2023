<template>
  <div class="posts-container container col-10 col-sm-8 col-md-6 col-lg-4">
    <select class="form-control" v-model="selected" @change="updateGraph()">
      <option value="daily">Aggregate Daily</option>
      <option value="monthly">Aggregate Monthly</option>
    </select>

    <Line id="my-chart-id" :data="chartData" :options="chartOptions" />
  </div>
</template>

<script>
import { DateTime } from 'luxon';
import axios from 'axios';
import { Line } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, CategoryScale, LinearScale, PointElement);

export default {
  components: { Line },
  data() {
    return {
      selected: 'daily',
      chartOptions: {
        response: true,
      },
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Posts',
            backgroundColor: '#ACBAC7',
            data: []
          }
        ]
      },
    }
  },
  methods: {
    async getPosts() {
      let response = await this.axiosInstance.get("/api/posts/get-posts");
      return response.data;
    },
    getDaysAgo(date) {
      return Math.floor(DateTime.now().diff(date, ["days"]).toObject()["days"]);
    },
    getMonthsAgo(date) {
      return Math.floor(DateTime.now().diff(date, ["months"]).toObject()["months"]);
    },
    async updateGraph() {
      let posts = await this.getPosts();
      let dates = posts.map(post => DateTime.fromSQL(post["time"]));

      let labels = [];
      let data = [];

      if (this.selected == "daily") {
        for (let i = 0; i < 7; i++) {
          labels[i] = DateTime.now().minus({ days: 6 - i }).toFormat("M/d");
        }
        let daysAgo = dates.map(date => this.getDaysAgo(date));

        for (let i=6; i>=0; i--) {
          data[6 - i] = daysAgo.filter(x => x == i).length;
        }

      } else {
        for (let i = 0; i < 6; i++) {
          labels[i] = DateTime.now().minus({ days: 5 - i }).toFormat("MMM");
        }
        let monthsAgo = dates.map(date => this.getMonthsAgo(date));

        for (let i=5; i>=0; i--) {
          data[5 - i] = monthsAgo.filter(x => x == i).length;
        }
      }
      this.chartData = {
        labels: labels,
        datasets: [
          {
            label: 'Posts',
            backgroundColor: '#ACBAC7',
            data: data
          }
        ]
      }
    }
  },
  beforeMount() {
    this.updateGraph();
  }
}
</script>