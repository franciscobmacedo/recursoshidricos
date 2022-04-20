import axios from "axios";
// const BASE_URL = "https://snirhapi.herokuapp.com/";
// const BASE_URL = "https://api.recursoshidricos.pt/";
// const BASE_URL = "http://localhost:8000/";
const BASE_URL = process.env.VUE_APP_API;
const instance = axios.create({
  baseURL: BASE_URL,
});
export async function getNetworks() {
  console.log("getting networks");
  const response = await instance.get("v1/networks");
  return response.data;
}

export async function getStations(networkID) {
  console.log("getting stations for network: ", networkID);
  const response = await instance.get("v1/stations", {
    params: {
      network_uid: networkID,
      page_size: 1000,
    },
  });

  console.log(response.data.items);
  return response.data.items;
}

export async function getParameters(stationIDs = null) {
  return await instance
    .get("v1/parameters", {
      params: {
        station_uids: stationIDs,
      },
    })
    .then((response) => {
      return response.data.items;
    })
    .catch((err) => {
      console.log(err);
    });
}

export async function getData(stationID, parameterID, startDate, endDate) {
  const response = await instance.get("v1/data", {
    params: {
      station_uids: stationID,
      parameter_uids: parameterID,
      tmin: startDate,
      tmax: endDate,
    },
  });

  return response.data;
}
