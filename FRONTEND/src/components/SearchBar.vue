<template>
  <div class="search-bar">

    <input
      :value="searchTerm"
      @input="$emit('update:searchTerm', $event.target.value)"
      type="text"
      placeholder="Business name or keyword..."
    />

    <select
      :value="category"
      @change="$emit('update:category', $event.target.value)"
    >

      <option value="">
        All Categories
      </option>

      <option
        v-for="category in categories"
        :key="category.category_id"
        :value="category.category_name"
      >
        {{category.category_name}}
      </option>
    </select>


    <select
      :value="location"
      @change="$emit('update:location', $event.target.value)"
    >
      <option value="">All Locations</option>
      <option
      v-for="location in locations"
      :key="location.parish"
      :value="location.parish"
      >
      {{location.parish}}
      </option>
    </select>


    <button @click="search">
      Search
    </button>

  </div>
</template>


<script setup>

const props = defineProps({
  searchTerm: String,
  category: String,
  location: String,
  categories:{
    type:Array,
    default:()=>[]
  },
  locations:{
    type:Array,
    default:()=>[]
  }
});


const emit = defineEmits([
  "update:searchTerm",
  "update:category",
  "update:location",
  "search"
]);


function search() {

  emit("search", {
    searchTerm: props.searchTerm,
    category: props.category,
    location: props.location
  });

}
</script>

<style scoped>
.search-bar {
  max-width: 900px;
  margin: 0 auto 50px;
  display: flex;
  align-items: center;
  background: white;
  border-radius: 14px;
  padding: 8px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, .08);
}

.search-bar input {
  flex: 2;
  border: none;
  padding: 15px;
  font-size: 16px;
  outline: none;
}

.search-bar select {
  flex: 1;
  border: none;
  border-left: 1px solid #D6D0C8;
  padding: 15px;
  background: white;
  outline: none;
}

.search-bar button {
  padding: 15px 30px;
  border: none;
  border-radius: 10px;
  background: #8B5A3C;
  color: white;
  cursor: pointer;
}

.search-bar button:hover {
  background: #74482D;
}
</style>