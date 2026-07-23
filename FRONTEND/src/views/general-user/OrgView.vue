<template>
  <div class="page">

    <button class="back-btn" @click="$router.back()">
      ← Back
    </button>

    <div class="hero">

      <img
        class="hero-image"
        src="https://placehold.co/500x300"
        alt="Organization"
      />

    </div>

    <div class="content">

      <!-- LEFT -->

      <div class="left">

        <div class="tags">
          <span>Technology</span>
          <span>Retail</span>
        </div>

        <h1>CablePro Data Servs Ltd</h1>

        <div class="rating">

          ★★★★☆ <span>(4.6 · 28 reviews)</span>

        </div>

        <div class="location">

          📍 6 Cairo Street, Portmore, St. Catherine

        </div>

        <hr>

        <h2>About</h2>

        <p>

          CablePro Data Services has been providing technology
          solutions including networking, surveillance cameras,
          computer systems, software development, and IT support.

          We work with businesses and community organizations to
          deliver reliable digital solutions while supporting local
          economic growth.

        </p>

        <hr>

        <h2>Reviews</h2>

        <div class="review">

          <strong>★★★★★ John Brown</strong>

          <p>
            Excellent customer service and quick installation.
          </p>

        </div>

        <div class="review">

          <strong>★★★★☆ Sarah Williams</strong>

          <p>
            Very knowledgeable staff.
          </p>

        </div>

      </div>

      <!-- RIGHT -->

      <div class="sidebar">

        <button class="save-btn">

          ❤️ Save

        </button>

        <button class="contact-btn">

          Get in Touch

        </button>

        <div class="info">

          <h3>Opening Hours</h3>

          <p>Mon–Fri</p>

          <p>8:30 AM – 5:00 PM</p>

          <br>

          <h3>Location</h3>
          <p>6 Cairo Street</p>
          <p>Portmore</p>
          <p>St. Catherine</p>
          <br>
          <h3>Phone</h3>
          <p>(876) 939-3852</p>
          <br>
          <h3>Website</h3>
          <a href="#">
            www.cableprodataservices.com
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

.page{
  background:#F6F2ED;
  min-height:100vh;
  padding:30px 50px;
}

.back-btn{
  background:none;
  border:none;
  color:#8B5A3C;
  cursor:pointer;
  margin-bottom:30px;
  font-size:15px;
}

.hero{
  display:flex;
  justify-content:center;
  margin-bottom:40px;
}

.hero-image{
  width:420px;
  border-radius:15px;
  box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.content{
  display:grid;
  grid-template-columns:2fr 350px;
  gap:40px;
}

.left{
  background:white;
  padding:30px;
  border-radius:18px;
  box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.tags{
  display:flex;
  gap:10px;
  margin-bottom:15px;
}

.tags span{
  background:#EEE6DE;
  color:#8B5A3C;
  padding:6px 14px;
  border-radius:20px;
  font-size:13px;
}

h1{
  color:#2C2C2C;
  margin-bottom:10px;
}

.rating{
  color:#8B5A3C;
  margin-bottom:10px;
}

.location{
  color:#666;
  margin-bottom:20px;
}

h2{
  color:#2C2C2C;
  margin-top:25px;
}

p{
  line-height:1.7;
  color:#555;
}

.review{
  margin-top:20px;
  padding:15px;
  background:#FAFAFA;
  border-radius:10px;
}

.sidebar{
  align-self:start;
  position:sticky;
  top:30px;
  background:white;
  padding:25px;
  border-radius:18px;
  box-shadow:0 10px 30px rgba(0,0,0,.08);
}

.save-btn,
.contact-btn{
  width:100%;
  margin-bottom:15px;
  padding:14px;
  border:none;
  border-radius:10px;
  background:#8B5A3C;
  color:white;
  cursor:pointer;
  font-size:15px;

}

.save-btn:hover,
.contact-btn:hover{
  background:#74482D;
}

.info{
  margin-top:20px;
}

.info h3{
  margin-bottom:5px;
  color:#2C2C2C;
}

.info a{
  color:#8B5A3C;
  text-decoration:none;
}

hr{
  margin:30px 0;
  border:none;
  border-top:1px solid #DDD;
}

@media(max-width:900px){
  .content{
    grid-template-columns:1fr;
}

.sidebar{
  position:relative;
}

.hero-image{
  width:100%;
  }

}

</style>