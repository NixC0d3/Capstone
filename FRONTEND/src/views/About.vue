<template>

<div class="about-page">
    <section class="hero">
        <div class="hero-text">
            <h1>
                Connecting Communities,
                Supporting Local Growth
            </h1>
            <p>
                CivilInfoHub helps people discover local businesses
                and charities while creating stronger community
                connections.
            </p>
        </div>

        <div class="hero-image">
            <img 
            src=""
            alt="Community"
            />
        </div>
    </section>

    <section class="mission">
        <h2>
            Our Mission
        </h2>

        <div class="cards">

            <div class="card">
                <h3>
                    Support Local Businesses
                </h3>
                <p>
                    Helping users find and support businesses
                    within their community.
                </p>
            </div>

            <div class="card">
                <h3>
                    Support Charities
                </h3>
                <p>
                    Connecting people with organisations
                    making a positive impact.
                </p>
            </div>

            <div class="card">
                <h3>
                    Personalised Discovery
                </h3>
                <p>
                    Recommendations help users discover
                    organisations relevant to them.
                </p>
            </div>
        </div>
    </section>

    <section class="team">
        <h2>
            Our Team
        </h2>

        <div class="team-grid">
            <div class="person">
                <div class="avatar"></div>
                <h4>
                    Sheri-Lee Mills
                </h4>
                <p>
                    Project Developer
                </p>
            </div>

            <div class="person">
                <div class="avatar"></div>
                <h4>
                    Melissa Grant
                </h4>
                <p>
                    Frontend Developer
                </p>
            </div>

            <div class="person">
                <div class="avatar"></div>
                <h4>
                    Hosea Nicols
                </h4>
                <p>
                    Backend Manager
                </p>
            </div>
        </div>
    </section>

</div>

</template>



<style scoped>

.about-page{

    background:#F6F2ED;

    min-height:100vh;

}


.hero{

    display:flex;

    justify-content:space-between;

    align-items:center;

    padding:60px 10%;

    background:white;

}


.hero-text{

    max-width:550px;

}


h1{

    font-size:3rem;

    color:#2C2C2C;

}


p{

    color:#666;

    line-height:1.6;

}



.hero-image img{

    width:350px;

    border-radius:20px;

}



.mission{

    padding:50px 10%;

    text-align:center;

}


.cards{

    display:grid;

    grid-template-columns:repeat(3,1fr);

    gap:30px;

}


.card{

    background:white;

    padding:25px;

    border-radius:15px;

    box-shadow:0 8px 20px rgba(0,0,0,.08);

}



.team{

    padding:50px 10%;

    text-align:center;

    background:white;

}


.team-grid{

    display:grid;

    grid-template-columns:repeat(3,1fr);

    gap:40px;

}


.avatar{

    width:90px;

    height:90px;

    background:#ddd;

    border-radius:50%;

    margin:auto;

}



@media(max-width:900px){

    .hero{

        flex-direction:column;

        text-align:center;

    }


    .cards,
    .team-grid{

        grid-template-columns:1fr;

    }

}

</style>