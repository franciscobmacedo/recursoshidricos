<template>
  <v-app>
    <v-main>
      <v-container fill-height fluid>
        <v-row align="center" justify="center">
          <div class="text-h1">Coming soon</div>
        </v-row>
        <v-row align="center" justify="center">
          <div class="text-overline">check the <a :href="apiUrl">api</a></div>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  computed: {
    apiUrl() {
      return "https://api.recursoshidricos.pt";
      // return process.env.VUE_APP_API;
    },
  },
};
</script>
