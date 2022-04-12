import Vue from "vue";
import Vuex from "vuex";
import { getStations, getParameters } from "@/api.js";
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    stations: [],
    loadingStations: false,
    selectedStations: [],
    parameters: [],
    loadingParameters: false,
    selectedParameters: [],
  },
  getters: {
    selectedStationsIDs(state) {
      return state.selectedStations.map((station) => station.uid);
    },
  },
  mutations: {
    setStations(state, items) {
      state.stations = items;
    },
    setLoadingStations(state, loading) {
      state.loadingStations = loading;
    },
    setSelectedStations(state, items) {
      state.selectedStations = items;
    },
    setselectedStationsByID(state, stationIDs) {
      state.selectedStations = state.stations.filter((station) =>
        stationIDs.includes(station.uid)
      );
    },
    setParameters(state, items) {
      state.parameters = items;
    },
    setLoadingParameters(state, loading) {
      state.loadingParameters = loading;
    },
    setSelectedParameters(state, parameters) {
      state.selectedParameters = parameters;
    },
  },
  actions: {
    async getStations(context, networkID) {
      context.commit("setStations", []);
      context.commit("setSelectedStations", []);
      context.commit("setLoadingStations", true);
      const stations = await getStations(networkID);
      context.commit("setStations", stations);
      context.commit("setLoadingStations", false);
    },
    async getParameters(context) {
      context.commit("setLoadingParameters", true);
      const selectedStationsIDs = context.getters.selectedStationsIDs;
      let parameters;
      if (selectedStationsIDs.length > 0) {
        parameters = await getParameters(context.getters.selectedStationsIDs);
      } else {
        parameters = [];
      }
      context.commit("setParameters", parameters);

      context.commit("setLoadingParameters", false);
    },
  },
});
