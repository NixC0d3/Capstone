# CivilInfoHub src folder comments

This version of the src folder has comments added to the Vue files so the code is easier to explain.

## Components vs Views

### components/
Components are reusable building blocks. They are usually smaller pieces of interface that can be used on more than one page.

Examples:
- OrganisationCard.vue displays one organisation.
- ReviewForm.vue collects a rating and review.
- SearchFilter.vue collects search/filter values.
- AppHeader.vue is the shared navigation bar.

### views/
Views are full pages/screens that are connected to routes in src/router/index.js. Each view usually combines several components to build a complete page.

Examples:
- ExploreView.vue is the full Explore page.
- OrganisationDetailsView.vue is the full details page for one organisation.
- LoginView.vue is the login page.
- RecommendationsView.vue is the recommendations page.

Simple rule:
- Use components for reusable parts.
- Use views for full pages attached to URLs.
