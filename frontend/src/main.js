import Vue from "vue";
import App from "./ComingSoon.vue";
import vuetify from "./plugins/vuetify";
import "leaflet/dist/leaflet.css";
import store from "./store";

Vue.config.productionTip = false;

new Vue({
  vuetify,
  store,
  render: (h) => h(App),
}).$mount("#app");
