<template>
  <section class="applications-card">
    <div class="section-header">
      <div>
        <h2>My Volunteer Applications</h2>
        <p>
          Track the opportunities you signed up for. Approved items are confirmed allocations.
        </p>
      </div>

      <button class="refresh-btn" @click="loadApplications">
        Refresh
      </button>
    </div>

    <p v-if="loading" class="status-message">
      Loading volunteer applications...
    </p>

    <p v-else-if="applications.length === 0" class="status-message">
      You have not signed up for any volunteer opportunities yet.
    </p>

    <div v-else class="application-list">
      <article
        v-for="application in applications"
        :key="application.signup_id"
        class="application-item"
      >
        <div class="application-top">
          <div>
            <p class="organisation-name">
              {{ application.organisation_name }}
            </p>

            <h3>{{ application.title }}</h3>
          </div>

          <span class="status-pill" :class="application.final_status">
            {{ formatStatus(application.final_status) }}
          </span>
        </div>

        <p class="description">
          {{ application.description || "No description provided." }}
        </p>

        <div class="details-grid">
          <p><strong>Date:</strong> {{ formatDate(application.needed_date) }}</p>
          <p><strong>Time:</strong> {{ formatTimeRange(application.start_time, application.end_time) }}</p>
          <p><strong>Location:</strong> {{ formatLocation(application) }}</p>

          <p v-if="application.final_status === 'approved'">
            <strong>Match Score:</strong> {{ application.matching_score }}/100
          </p>
        </div>

        <div class="skills">
          <span
            v-for="skill in application.required_skills"
            :key="skill"
            class="skill-pill"
          >
            {{ skill }}
          </span>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { api } from "@/services/api";

const applications = ref([]);
const loading = ref(false);

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

function formatLocation(application) {
  const parts = [application.town, application.parish].filter(Boolean);
  return parts.length ? parts.join(", ") : "Location not specified";
}

function formatStatus(status) {
  if (status === "approved") {
    return "Approved Allocation";
  }

  if (status === "declined" || status === "rejected") {
    return "Declined";
  }

  if (status === "pending") {
    return "Pending Review";
  }

  return String(status || "pending").replace("_", " ");
}


async function loadApplications() {
  try {
    loading.value = true;

    const user = getCurrentUser();
    const userId = user.user_id || user.id;

    if (!userId) {
      applications.value = [];
      return;
    }

    const data = await api.getMyVolunteerApplications(userId);
    applications.value = Array.isArray(data) ? data : [];

  } catch (error) {
    console.error("Failed to load volunteer applications:", error);
    applications.value = [];
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadApplications();
});
</script>

<style scoped>
.applications-card {
  display: grid;
  gap: 18px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  align-items: flex-start;
}

.section-header h2 {
  margin: 0;
}

.section-header p {
  margin: 8px 0 0;
  color: #666;
}

.refresh-btn {
  background: #8b5a3c;
  color: white;
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
}

.status-message {
  color: #666;
}

.application-list {
  display: grid;
  gap: 18px;
}

.application-item {
  border: 1px solid #e7ddd2;
  border-radius: 14px;
  padding: 20px;
  background: #faf8f5;
}

.application-top {
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

.application-item h3 {
  margin: 0;
}

.description {
  color: #555;
  line-height: 1.45;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 4px 18px;
}

.status-pill {
  padding: 7px 12px;
  border-radius: 999px;
  font-weight: 700;
  font-size: 13px;
  text-transform: capitalize;
  background: #fff3cd;
  color: #664d03;
  white-space: nowrap;
}

.status-pill.approved {
  background: #d1e7dd;
  color: #0f5132;
}

.status-pill.declined,
.status-pill.rejected,
.status-pill.cancelled {
  background: #f8d7da;
  color: #842029;
}

.skills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.skill-pill {
  background: #efe5db;
  color: #8b5a3c;
  padding: 6px 12px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
}
</style>
