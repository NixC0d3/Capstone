<template>
  <main class="volunteer-page">
    <section class="hero-card">
      <p class="eyebrow">Community service</p>
      <h1>Volunteer Opportunities</h1>
      <p class="subtitle">
        Browse open volunteer needs from charities and sign up for the ones you would like to support.
      </p>
    </section>

    <section class="opportunities-section">
      <div class="section-header">
        <h2>Available Opportunities</h2>

        <button class="refresh-btn" @click="loadOpportunities">
          Refresh
        </button>
      </div>

      <p v-if="loading" class="status-message">
        Loading opportunities...
      </p>

      <p v-else-if="opportunities.length === 0" class="status-message">
        No volunteer opportunities are currently available.
      </p>

      <div v-else class="opportunity-grid">
        <article
          v-for="opportunity in opportunities"
          :key="opportunity.volunteer_need_id"
          class="opportunity-card"
        >
          <div class="card-top">
            <div>
              <p class="organisation-name">
                {{ opportunity.organisation_name }}
              </p>

              <h3>{{ opportunity.title }}</h3>
            </div>

            <span class="urgency-pill" :class="opportunity.urgency_level">
              {{ opportunity.urgency_level || "medium" }}
            </span>
          </div>

          <p class="description">
            {{ opportunity.description || "No description provided." }}
          </p>

          <div class="details">
            <p><strong>Date:</strong> {{ formatDate(opportunity.needed_date) }}</p>
            <p><strong>Time:</strong> {{ formatTimeRange(opportunity.start_time, opportunity.end_time) }}</p>
            <p><strong>Location:</strong> {{ formatLocation(opportunity) }}</p>
            <p><strong>Volunteers needed:</strong> {{ opportunity.volunteers_needed || 1 }}</p>
          </div>

          <div class="skills">
            <span
              v-for="skill in opportunity.required_skills"
              :key="skill"
              class="skill-pill"
            >
              {{ skill }}
            </span>

            <span
              v-if="!opportunity.required_skills || !opportunity.required_skills.length"
              class="empty-skills"
            >
              No specific skills listed
            </span>
          </div>

          <button
            class="signup-btn"
            :disabled="opportunity.already_signed_up || signingUpId === opportunity.volunteer_need_id"
            @click="apply(opportunity)"
          >
            {{ buttonText(opportunity) }}
          </button>
        </article>
      </div>
    </section>
  </main>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { api } from "@/services/api";

const router = useRouter();

const opportunities = ref([]);
const loading = ref(false);
const signingUpId = ref(null);

function getCurrentUser() {
  return JSON.parse(localStorage.getItem("user") || "{}");
}

function formatDate(dateValue) {
  if (!dateValue) {
    return "Date not specified";
  }

  return new Date(dateValue).toLocaleDateString(undefined, {
    year: "numeric",
    month: "long",
    day: "numeric"
  });
}

function formatTimeRange(startTime, endTime) {
  if (!startTime && !endTime) {
    return "Time not specified";
  }

  if (startTime && endTime) {
    return `${startTime} - ${endTime}`;
  }

  return startTime || endTime;
}

function formatLocation(opportunity) {
  const parts = [opportunity.town, opportunity.parish].filter(Boolean);
  return parts.length ? parts.join(", ") : "Location not specified";
}

function normaliseStatus(status) {
  return String(status || "").replace("_", " ");
}

function buttonText(opportunity) {
  if (signingUpId.value === opportunity.volunteer_need_id) {
    return "Signing up...";
  }

  if (opportunity.already_signed_up) {
    const status = normaliseStatus(opportunity.application_status || "pending");
    return `Already signed up (${status})`;
  }

  return "Sign Up";
}

async function loadOpportunities() {
  try {
    loading.value = true;

    const user = getCurrentUser();
    const userId = user.user_id || user.id;

    if (!userId) {
      router.push("/login");
      return;
    }

    const data = await api.getVolunteerOpportunities(userId);
    opportunities.value = Array.isArray(data) ? data : [];

  } catch (error) {
    console.error("Error loading opportunities:", error);
    opportunities.value = [];
  } finally {
    loading.value = false;
  }
}

async function apply(opportunity) {
  try {
    const user = getCurrentUser();
    const userId = user.user_id || user.id;

    if (!userId) {
      router.push("/login");
      return;
    }

    signingUpId.value = opportunity.volunteer_need_id;

    await api.signupVolunteer({
      user_id: userId,
      volunteer_need_id: opportunity.volunteer_need_id
    });

    opportunity.already_signed_up = true;
    opportunity.application_status = "pending";

    alert("Your volunteer application was submitted. The charity can now review and approve it.");

  } catch (error) {
    console.error("Volunteer application failed:", error);
    alert(error.message || "Volunteer application failed.");
  } finally {
    signingUpId.value = null;
  }
}

onMounted(() => {
  loadOpportunities();
});
</script>

<style scoped>
.volunteer-page {
  min-height: 100vh;
  padding: 40px;
  background: #f6f2ed;
}

.hero-card {
  text-align: center;
  background: white;
  border-radius: 20px;
  padding: 45px 30px;
  margin-bottom: 35px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.06);
}

.eyebrow {
  color: #8b5a3c;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin: 0 0 10px;
}

h1 {
  margin: 0;
  font-size: 42px;
  color: #2c2c2c;
}

.subtitle {
  color: #666;
  margin-top: 12px;
}

.opportunities-section {
  max-width: 1200px;
  margin: auto;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.refresh-btn,
.signup-btn {
  background: #965f3f;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
}

.signup-btn:disabled {
  background: #b9a99f;
  cursor: not-allowed;
}

.status-message {
  background: white;
  padding: 25px;
  border-radius: 14px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
}

.opportunity-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 22px;
}

.opportunity-card {
  background: white;
  padding: 25px;
  border-radius: 16px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.08);
}

.card-top {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: flex-start;
}

.organisation-name {
  color: #8b5a3c;
  font-weight: 700;
  margin: 0 0 8px;
}

.opportunity-card h3 {
  margin: 0;
  font-size: 22px;
}

.urgency-pill {
  padding: 6px 12px;
  border-radius: 999px;
  background: #efe5db;
  color: #8b5a3c;
  font-size: 13px;
  font-weight: 700;
  text-transform: capitalize;
}

.urgency-pill.high {
  background: #f8d7da;
  color: #842029;
}

.urgency-pill.medium {
  background: #fff3cd;
  color: #664d03;
}

.urgency-pill.low {
  background: #d1e7dd;
  color: #0f5132;
}

.description {
  color: #555;
  line-height: 1.45;
}

.details p {
  margin: 8px 0;
}

.skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 16px 0;
}

.skill-pill {
  background: #efe5db;
  color: #8b5a3c;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
}

.empty-skills {
  color: #777;
  font-style: italic;
}
</style>
