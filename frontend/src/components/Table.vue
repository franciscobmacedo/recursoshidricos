<template>
  <div style="position: relative">
    <v-row class="py-0 px-0 my-0 mx-0" align="center">
      <v-col cols="12" class="py-0">
        <v-text-field
          v-model="search"
          append-icon="mdi-magnify"
          :label="searchPlaceholder"
          single-line
          hide-details
        ></v-text-field>
      </v-col>
      <v-col class="py-0">
        <v-switch
          :disabled="!hasSelectedItems"
          v-model="showOnlySelected"
          :label="onlySelectedLable"
        ></v-switch>
      </v-col>

      <v-col v-if="hasSelectedItems" class="py-0">
        <v-btn color="red" dark small @click="clearSelection">
          <v-icon>mdi-close</v-icon> Apagar seleção
        </v-btn>
      </v-col>
    </v-row>

    <v-data-table
      v-model="_selectedItems"
      :loading="loadingItems"
      :headers="_headers"
      :items="_items"
      :search="search"
      show-select
      :show-expand="expandableFields !== undefined"
      :single-expand="expandableFields !== undefined"
    >
      <template v-slot:expanded-item="{ headers, item }">
        <td :colspan="headers.length">
          <v-list-item dense v-for="(field, i) in expandableFields" :key="i">
            <strong>{{ field }}</strong
            >: {{ item[field] }}
          </v-list-item>
        </td>
      </template>
    </v-data-table>
  </div>
</template>

<script>
export default {
  props: {
    headers: Array,
    items: Array,
    selectedItems: Array,
    loadingItems: Boolean,
    searchPlaceholder: {
      type: String,
      default: "Procurar",
    },
    onlySelectedLable: {
      type: String,
      default: "Mostrar só selecionados",
    },
    expandableFields: Array,
    selectedHelperText: {
      type: String,
      default: "selecionados",
    },
  },
  data() {
    return {
      search: "",
      showOnlySelected: false,
    };
  },
  computed: {
    _selectedHelperText() {
      return `${this.selectedItems.length} ${this.selectedHelperText}`;
    },
    _headers() {
      return [...this.headers, { text: "", value: "data-table-expand" }];
    },
    _selectedItems: {
      set(items) {
        this.$emit("selectItems", items);
      },
      get() {
        return this.selectedItems;
      },
    },
    _items() {
      return this.showOnlySelected ? this.selectedItems : this.items;
    },
    hasSelectedItems() {
      return this.selectedItems.length > 0;
    },
  },
  methods: {
    clearSelection() {
      this.showOnlySelected = false;
      this.$emit("clearSelection");
    },
  },
};
</script>

<style>
.v-label {
  font-size: 12px;
}
.v-data-footer {
  justify-content: end;
}
.bottom-text {
  position: absolute;
  bottom: 0;
  left: 0;
  display: flex;
  max-width: 50rem;
  flex-wrap: wrap;
}
</style>