<template>
  <div>
    <v-menu
      ref="menu"
      v-model="menu"
      :close-on-content-click="false"
      transition="scale-transition"
      offset-y
      min-width="auto"
    >
      <template v-slot:activator="{ on, attrs }">
        <v-text-field
          v-model="date"
          :label="name"
          prepend-icon="mdi-calendar"
          readonly
          v-bind="attrs"
          v-on="on"
        ></v-text-field>
      </template>
      <v-date-picker
        v-model="date"
        :active-picker.sync="activePicker"
        :max="
          new Date(Date.now() - new Date().getTimezoneOffset() * 60000)
            .toISOString()
            .substr(0, 10)
        "
        :min="minDate"
        @input="menu = false"
      ></v-date-picker>
    </v-menu>
  </div>
</template>
<script>
export default {
  props: {
    name: String,
    dateProps: String,
    minDate: {
      type: String,
      default: "1920-01-01",
    },
  },
  data: () => ({
    activePicker: null,
    menu: false,
  }),
  computed: {
    date: {
      get() {
        return this.dateProps;
      },
      set(value) {
        this.$emit("setDate", value);
      },
    },
  },
  watch: {
    menu(val) {
      val && setTimeout(() => (this.activePicker = "YEAR"));
    },
    minDate(val) {
      const minDateVal = new Date(val);
      const dateVal = new Date(this.date);
      if (minDateVal > dateVal) {
        this.date = val;
      }
    },
  },
  // methods: {
  //   save(date) {
  //     this.menu = false;
  //   },
  // },
};
</script>