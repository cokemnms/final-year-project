<template>
  <v-sheet
    class="mx-auto custom-sheet"
    elevation="8"
  >
    <v-slide-group
      v-model="model"
      class="pa-4"
      
      show-arrows
    >
      <!-- Custom Previous Arrow -->
      <template #prev>
        <v-btn icon color="black">
          <v-icon size="36px" color="white">mdi-chevron-left</v-icon>
        </v-btn>
      </template>

      <!-- Slide Group Items -->
      <v-slide-group-item
        v-for="(item, index) in items"
        :key="index"
        v-slot="{ isSelected, toggle, selectedClass }"
      >
        <v-card
          :class="['ma-4', selectedClass]"
          color="grey-lighten-3"
          height="300"
          width="200"
          @click="toggle"
        >
          <div class="relative">
            <v-img
              :src="item.image"
              height="150"
              contain
            ></v-img>
            <v-icon
              v-if="item.isFavorite"
              color="red"
              class="favorite-icon"
              @click.stop="toggleFavorite(index)"
            >
              mdi-heart
            </v-icon>
            <v-icon
              v-else
              color="grey"
              class="favorite-icon"
              @click.stop="toggleFavorite(index)"
            >
              mdi-heart-outline
            </v-icon>
          </div>
          <v-card-text class="pa-2">
            <div class="text-h6">{{ item.name }}</div>
            <div class="text-subtitle-2 text-success">
              ${{ item.price }}
            </div>
            <div class="text-caption text-grey">
              {{ item.timeAgo }} ago
            </div>
            <v-rating
              :value="item.rating"
              dense
              color="yellow"
              readonly
              class="mt-1"
            ></v-rating>
          </v-card-text>
        </v-card>
      </v-slide-group-item>

      <!-- Custom Next Arrow -->
      <template #next>
        <v-btn icon color="red">
          <v-icon size="36" color="white">mdi-chevron-right</v-icon>
        </v-btn>
      </template>
    </v-slide-group>
  </v-sheet>
</template>

<script>
export default {
  name: "CategoryProducts",
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    model: null,
  }),
  methods: {
    toggleFavorite(index) {
      this.$emit("update-favorite", index);
    },
  },
};
</script>

<style scoped>
.custom-sheet {
  margin-top: 300px;
  width: 96vw;
  border-radius: 30px;
}
.favorite-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  cursor: pointer;
  font-size: 24px;
}
</style>
