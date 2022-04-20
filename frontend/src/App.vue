<template>
  <v-app>
    <v-app-bar app color="white" dense>
      <div class="d-flex align-center">Recursos Hídricos</div>

      <v-spacer></v-spacer>
      <v-btn href="https://snirh.apambiente.pt/" target="_blank" text>
        <span class="mr-2">Dados recolhidos no stie original</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <v-row>
          <v-col sm="12" md="3">
            <v-autocomplete
              :loading="loadingNetworks"
              v-model="network"
              :items="networks"
              item-text="nome"
              @change="getNetworkStations"
              return-object
              placeholder="Rede"
              label="Rede"
            ></v-autocomplete>
            <Map />
          </v-col>
          <!-- <v-col>
            <v-row>
              <v-col sm="12" md="8">
                <Table
                  v-show="network"
                  :headers="stationsHeaders"
                  :items="stations"
                  :selectedItems="selectedStations"
                  :loadingItems="loadingStations"
                  @selectItems="setSelectedStations"
                  @clearSelection="setSelectedStations"
                  searchPlaceholder="Procurar estações"
                  onlySelectedLable="Mostrar só selecionadas"
                  selectedHelperText="estações selecionadas"
                  :expandableFields="expandableFields"
                />
              </v-col>
              <v-divider vertical v-show="network"></v-divider>
              <v-col sm="12" md="4">
                <Table
                  v-show="network"
                  :headers="parametersHeaders"
                  :items="parameters"
                  :selectedItems="selectedParameters"
                  :loadingItems="loadingParameters"
                  @selectItems="setSelectedParameters"
                  @clearSelection="setSelectedParameters"
                  selectedHelperText="parâmetros selecionados"
                  searchPlaceholder="Procurar parâmetros"
                />
              </v-col>
            </v-row>
            <v-row v-show="network" align="center" justify="center">
              <v-col md="2">
                <v-chip color="green lighten-1" dark>
                  {{ selectedStations.length }} estações selecionadas
                </v-chip>
              </v-col>
              <v-col md="2">
                <v-chip color="blue lighten-1" dark>
                  {{ selectedParameters.length }} parametros selecionados
                </v-chip>
              </v-col>

              <v-col md="2">
                <DatePicker
                  name="Data de início"
                  @setDate="setStartDate"
                  :dateProps="startDate"
                />
              </v-col>
              <v-col md="2">
                <DatePicker
                  name="Data de fim"
                  @setDate="setEndDate"
                  :dateProps="endDate"
                  :minDate="startDate"
                />
              </v-col>
              <v-col md="2">
                <v-btn
                  color="primary"
                  :disabled="loadingData"
                  @click="getData()"
                >
                  <v-icon>mdi-download</v-icon>
                  Transferir dados
                </v-btn>
              </v-col>
            </v-row>
          </v-col> -->
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters, mapState } from "vuex";
import { getNetworks, getData } from "@/api.js";
import DatePicker from "@/components/DatePicker.vue";
import Map from "@/components/Map.vue";
// import Table from "@/components/Table.vue";

export default {
  name: "App",
  components: {
    Map,
    DatePicker,
    // Table,
  },

  data: () => ({
    networks: [],
    network: null,
    loadingNetworks: true,

    startDate: "1980-01-01",
    endDate: "2020-12-31",

    loadingData: false,
    showAlert: false,

    stationsHeaders: [
      { text: "Estação", value: "nome" },
      { text: "Codigo", value: "codigo" },
      { text: "Latitude", value: "latitude" },
      { text: "Longitude", value: "longitude" },
      { text: "Altitude (m)", value: "altitude" },
    ],
    expandableFields: [
      "id",
      "codigo",
      "nome",
      "altitude",
      "latitude",
      "longitude",
      "coord_x",
      "coord_y",
      "bacia",
      "distrito",
      "concelho",
      "freguesia",
      "entidade_responsavel_automatica",
      "entidade_responsavel_convencional",
      "tipo_estacao_automatica",
      "tipo_estacao_convencional",
      "entrada_funcionamento_automatica",
      "telemetria",
      "estado",
    ],
    parametersHeaders: [{ text: "Parametro", value: "nome" }],
  }),
  async created() {
    this.loadingNetworks = true;
    this.networks = await getNetworks();
    this.loadingNetworks = false;
  },
  computed: {
    ...mapState([
      "selectedStations",
      "stations",
      "loadingStations",
      "parameters",
      "loadingParameters",
      "selectedParameters",
    ]),
    ...mapGetters(["selectedStationsIDs"]),
  },
  methods: {
    isDetailParam(parameter) {
      if (parameter === null) {
        return false;
      }
      return ["diário", "horário", "diária", "horária", "hora", "dia"].map(
        (s) => {
          parameter.nome.includes(s);
        }
      );
    },
    setSelectedStations(stations) {
      this.$store.commit(
        "setSelectedStations",
        stations === undefined ? [] : stations
      );
      this.$store.dispatch("getParameters");
    },
    setSelectedParameters(parameters) {
      this.$store.commit(
        "setSelectedParameters",
        parameters === undefined ? [] : parameters
      );
    },

    async getNetworkStations() {
      await this.$store.dispatch("getStations", this.network.uid);
    },
    async getData() {
      this.loadingData = true;
      const data = [];
      this.selectedStationsIDs.map(async (stationID) => {
        const stationData = await getData(
          stationID,
          this.selectedParameters[0].uid,
          this.startDate,
          this.endDate
        );
        data.push(stationData);
      });
      console.log("final data", data);
      this.loadingData = false;
    },
    setStartDate(date) {
      this.startDate = date;
      const startDate = new Date(this.startDate);
      const endDate = new Date(this.endDate);
      if (endDate < startDate) {
        this.endDate = this.formatDate(this.getDateMonthsLater(startDate));
      }
    },
    setEndDate(date) {
      const isValid = this.validateEndDate(date);
      if (!isValid) {
        this.showAlert = true;
      }
    },
    validateEndDate(_endDate = null) {
      if (this.isDetailParam()) {
        //change this if necessary
        const startDate = new Date(this.startDate);
        let endDate = new Date(_endDate || this.endDate);
        const monthDiff = this.monthDiff(startDate, endDate);
        if (monthDiff > 2) {
          this.endDate = this.formatDate(this.getDateMonthsLater(startDate));
          return false;
        } else {
          this.endDate = this.formatDate(endDate);
        }
      }
      return true;
    },
    monthDiff(d1, d2) {
      var months;
      months = (d2.getFullYear() - d1.getFullYear()) * 12;
      months -= d1.getMonth();
      months += d2.getMonth();
      return months <= 0 ? 0 : months;
    },
    getDateMonthsLater(date, nrMonths = 2) {
      const date2 = new Date(date.getTime());
      date2.setMonth(date2.getMonth() + nrMonths);
      return date2;
    },
    formatDate(date) {
      return `${date.getFullYear()}-${this.zeroPad(
        date.getMonth() + 1
      )}-${this.zeroPad(date.getDate())}`;
    },
    zeroPad(num, places = 2) {
      return String(num).padStart(places, "0");
    },
  },
};
</script>
