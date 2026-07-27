<template>
  <main class="page">
    <h1>Volunteer Allocation</h1>
    
    <section class="form-card">
	  <h2>Create Volunteer Need</h2>

	  <form @submit.prevent="createNeed">
		<label>Title</label>
		<input v-model="newNeed.title" type="text" required />

		<label>Description</label>
		<textarea v-model="newNeed.description"></textarea>

		<label>Urgency</label>
		<select v-model="newNeed.urgency_level">
		  <option value="low">Low</option>
		  <option value="medium">Medium</option>
		  <option value="high">High</option>
		</select>

		<label>Needed Date</label>
		<input v-model="newNeed.needed_date" type="date" />

		<label>Start Time</label>
		<input v-model="newNeed.start_time" type="time" />

		<label>End Time</label>
		<input v-model="newNeed.end_time" type="time" />

		<label>Volunteers Needed</label>
		<input v-model.number="newNeed.volunteers_needed" type="number" min="1" />

		<label>Required Skills</label>
		<input
		  v-model="skillsText"
		  type="text"
		  placeholder="Example: First Aid, Construction, Driving"
		/>

		<button type="submit">
		  Create Volunteer Need
		</button>
	  </form>
	</section>

    <section class="need-list">
      <h2>Volunteer Needs</h2>

      <p v-if="loadingNeeds">
        Loading volunteer needs...
      </p>

      <p v-else-if="needs.length === 0">
        No volunteer needs found.
      </p>

      <div
        v-for="needItem in needs"
        :key="needItem.volunteer_need_id"
        class="need-card"
        :class="{ selected: selectedNeedId === needItem.volunteer_need_id }"
      >
        <h3>{{ needItem.title }}</h3>

        <p>
          <strong>Charity:</strong> {{ needItem.organisation_name }}
        </p>

        <p>
          <strong>Volunteers needed:</strong> {{ needItem.volunteers_needed }}
        </p>

        <p>
          <strong>Urgency:</strong> {{ needItem.urgency_level }}
        </p>

        <p>
          <strong>Skills:</strong>
          {{
            needItem.required_skills.length
              ? needItem.required_skills.join(", ")
              : "No skills listed"
          }}
        </p>

        <button @click="selectNeed(needItem.volunteer_need_id)">
          Find Matching Volunteers
        </button>
      </div>
    </section>

    <section v-if="selectedNeedId" ref="matchesSection" class="matches-section">
      <h2>Recommended Volunteers</h2>

      <p v-if="loadingMatches">
        Loading matches...
      </p>

      <p v-else-if="matches.length === 0">
        No matching volunteers found.
      </p>

      <div v-else class="matches-grid">
        <div
          v-for="match in matches"
          :key="match.user_id"
          class="match-card"
        >
          <h3>{{ match.display_name }}</h3>

          <p>
            <strong>Email:</strong> {{ match.email }}
          </p>

          <p>
            <strong>Location:</strong>
            {{ match.user_town || "Unknown" }},
            {{ match.user_parish || "Unknown" }}
          </p>

          <p>
            <strong>User skills:</strong>
            {{
              match.user_skills.length
                ? match.user_skills.join(", ")
                : "No skills listed"
            }}
          </p>

          <p>
            <strong>Matched skills:</strong>
            {{
              match.matched_skills.length
                ? match.matched_skills.join(", ")
                : "None"
            }}
          </p>

          <div class="score-box">
            <p>Skill Score: {{ match.skill_score }}</p>
            <p>Cause Score: {{ match.cause_score }}</p>
            <p>Location Score: {{ match.location_score }}</p>
            <p>Availability Score: {{ match.availability_score }}</p>
            <h4>Total Match Score: {{ match.match_score }}</h4>
          </div>

          <button @click="allocate(match)">
            Allocate Volunteer
          </button>
        </div>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import { api } from "@/services/api";

const needs = ref([]);
const matches = ref([]);
const matchesSection = ref(null);

const selectedNeedId = ref(null);

const loadingNeeds = ref(false);
const loadingMatches = ref(false);

const newNeed = ref({
  title: "",
  description: "",
  urgency_level: "medium",
  needed_date: "",
  start_time: "",
  end_time: "",
  volunteers_needed: 1
});

const skillsText = ref("");

async function createNeed() {
  try {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const charityUserId = user.user_id || user.id;

    if (!charityUserId) {
      alert("No logged-in charity user found.");
      return;
    }

    const requiredSkills = skillsText.value
      .split(",")
      .map(skill => skill.trim())
      .filter(skill => skill.length > 0);

    await api.createVolunteerNeed({
      charity_user_id: charityUserId,
      title: newNeed.value.title,
      description: newNeed.value.description,
      urgency_level: newNeed.value.urgency_level,
      needed_date: newNeed.value.needed_date || null,
      start_time: newNeed.value.start_time || null,
      end_time: newNeed.value.end_time || null,
      volunteers_needed: newNeed.value.volunteers_needed,
      required_skills: requiredSkills
    });

    alert("Volunteer need created successfully.");

    newNeed.value = {
      title: "",
      description: "",
      urgency_level: "medium",
      needed_date: "",
      start_time: "",
      end_time: "",
      volunteers_needed: 1
    };

    skillsText.value = "";

    await loadVolunteerNeeds();
  } catch (error) {
    console.error("Error creating volunteer need:", error);
    alert("Volunteer need was not created.");
  }
}

async function loadVolunteerNeeds() {
  try {
    loadingNeeds.value = true;

    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const charityUserId = user.user_id || user.id;

    if (!charityUserId) {
      console.error("No logged-in charity user found.");
      needs.value = [];
      return;
    }

    const data = await api.getVolunteerNeeds(charityUserId);

    needs.value = Array.isArray(data) ? data : [];

    console.log("Volunteer needs:", needs.value);
  } catch (error) {
    console.error("Error loading volunteer needs:", error);
    needs.value = [];
  } finally {
    loadingNeeds.value = false;
  }
}

async function selectNeed(volunteerNeedId) {
  try {
    selectedNeedId.value = volunteerNeedId;
    loadingMatches.value = true;
    matches.value = [];

    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const charityUserId = user.user_id || user.id;

    const data = await api.getVolunteerMatches(volunteerNeedId, charityUserId);
    matches.value = data.matches || [];
    
    await nextTick();

    matchesSection.value?.scrollIntoView({
      behavior: "smooth",
      block: "start"
    });

    console.log("Selected need:", data.need);
    console.log("Volunteer matches:", matches.value);
  } catch (error) {
    console.error("Error loading volunteer matches:", error);
    matches.value = [];
  } finally {
    loadingMatches.value = false;
  }
}

async function allocate(match) {
  try {
    const user = JSON.parse(localStorage.getItem("user") || "{}");
    const charityUserId = user.user_id || user.id;

    await api.allocateVolunteer(selectedNeedId.value, {
      user_id: match.user_id,
      match_score: match.match_score,
      charity_user_id: charityUserId
    });

    alert(`${match.display_name} was allocated successfully.`);
  } catch (error) {
    console.error("Error allocating volunteer:", error);
    alert("Volunteer allocation failed.");
  }
}

onMounted(() => {
  loadVolunteerNeeds();
});
</script>

<style scoped>
.page {
  padding: 40px;
}

.need-list {
  margin-bottom: 40px;
}

.need-card,
.match-card {
  background: white;
  padding: 20px;
  border-radius: 14px;
  margin-bottom: 20px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

.need-card.selected {
  border: 2px solid #965f3f;
}

.matches-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 20px;
}

.score-box {
  background: #f5f1ed;
  padding: 12px;
  border-radius: 10px;
  margin: 12px 0;
}

button {
  background: #965f3f;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
}

.form-card {
  background: white;
  padding: 24px;
  border-radius: 14px;
  margin-bottom: 30px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
}

form {
  display: grid;
  gap: 12px;
  max-width: 600px;
}

input,
textarea,
select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: inherit;
}

textarea {
  min-height: 90px;
}
</style>
