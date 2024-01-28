import streamlit as st


def render_docs(docs:list):

    #First column
    fc1 = st.columns([0.4,0.3,0.3])

    if len (docs) > 0:
        with fc1[0]:
            with st.container(border=True):
                st.write(f"## {docs[0]}")

    if len (docs) > 1:
        with fc1[1]:
            with st.container(border=True):
                st.write(f"## {docs[1]}")


#------------------------------------------BODY------------------------------------------------------------

headcols = st.columns([0.7,0.3])
with headcols[0]:
    with open('rsc/html/docs_home_header.html') as f:
        st.markdown(f.read(), unsafe_allow_html=True)

headcols[1].markdown('''
<div style="display: flex; justify-content: center; align-items: center;padding-top: 50px;">
    <h1 style="font-family: 'Roboto'; font-size: 10vw;text-align: center;align-items: center;justify-content: center;">
    Blog
    </h1>
</div>
''', unsafe_allow_html=True)

st.divider()



st.markdown('''
<style>
@import url(https://fonts.googleapis.com/css?family=Roboto);
/* The card */
.cardtwo {
  position: relative;
  height: 450px;
  width: 900px;
  margin: 200px auto;
  background-color: #FFF;
  -webkit-box-shadow: 10px 10px 93px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 10px 10px 93px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 10px 10px 93px 0px rgba(0, 0, 0, 0.75);
}
/* Image on the left side */
.thumbnail {
  float: left;
  position: relative;
  left: 30px;
  top: -30px;
  height: 320px;
  width: 530px;
  -webkit-box-shadow: 10px 10px 60px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 10px 10px 60px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 10px 10px 60px 0px rgba(0, 0, 0, 0.75);
  overflow: hidden;
}
/*object-fit: cover;*/
/*object-position: center;*/
img.left {
  position: absolute;
  left: 50%;
  top: 50%;
  height: auto;
  width: 100%;
  -webkit-transform: translate(-50%, -50%);
  -ms-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
}
/* Right side of the card */
.right {
  margin-left: 590px;
  margin-right: 20px;
}
.cardtwo h1 {
  padding-top: 15px;
  font-size: 1.3rem;
  color: #4B4B4B;
}
.author {
  background-color: #9ECAFF;
  height: 30px;
  width: 110px;
  border-radius: 20px;
}
.author h2 {
    padding-top: 5px;
}
.author > img {
  padding-top: 5px;
  margin-left: 10px;
  float: left;
  height: 20px;
  width: 20px;
  border-radius: 50%;
}
.right h2 {
  padding-top: 8px;
  margin-right: 6px;
  text-align: right;
  font-size: 0.8rem;
}
.separator {
  margin-top: 10px;
  border: 1px solid #C3C3C3;
}
.cardtwo p {
  text-align: justify;
  padding-top: 10px;
  font-size: 0.75rem;
  line-height: 150%;
  color: #4B4B4B;
}
/* DATE of release*/
.right h5 {
  position: absolute;
  left: 30px;
  bottom: 0px;
  font-size: 6rem;
  color: #C3C3C3;
  top: 300px;
}
.right h6 {
  position: absolute;
  left: 30px;
  bottom: 0px;
  font-size: 2rem;
  color: #C3C3C3;
  bottom: -10px;
}
/* Those futur buttons */
.right ul {
  margin-left: 250px;
}
.right li {
  display: inline;
  list-style: none;
  padding-right: 40px;
  color: #7B7B7B;
}
/* Floating action button */
.fab {
  position: absolute;
  display: flex;
  justify-content: center;
  right: 50px;
  box-sizing: border-box;
  padding-top: 18px;
  background-color: #1875D0;
  width: 80px;
  height: 80px;
  color: white;
  text-align: center;
  border-radius: 50%;
  -webkit-box-shadow: 10px 10px 50px 0px rgba(0, 0, 0, 0.75);
  -moz-box-shadow: 10px 10px 50px 0px rgba(0, 0, 0, 0.75);
  box-shadow: 10px 10px 50px 0px rgba(0, 0, 0, 0.75);
  align-items: center;
}
</style>
''', unsafe_allow_html=True)


st.markdown(f'''
<div class="cardtwo">
    <div class="thumbnail">
        <img class="left" src="https://cdn2.hubspot.net/hubfs/322787/Mychefcom/images/BLOG/Header-Blog/photo-culinaire-pexels.jpg">
    </div>
    <div class="right">
        <h1>Why you Need More Magnesium in Your Daily Diet</h1>
        <div class="separator"></div>
        <p>Magnesium is one of the six essential macro-minerals that is required by the body for energy production and synthesis of protein and enzymes. It contributes to the development of bones and most importantly it is responsible for synthesis of your DNA and RNA. A new report that has appeared in theBritish Journal of Cancer, gives you another reason to add more magnesium to your diet...</p>
        <h5>28</h5>
        <h6>Aug</h6>
    </div>
    <div class="fab"><img src="https://cdn-icons-png.flaticon.com/128/1565/1565867.png" width="60"></div>
</div>

''', unsafe_allow_html=True)



st.markdown('''
<style>
@import url("https://fonts.googleapis.com/css2?family=Quicksand:wght@300..700&display=swap");
.containercard {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  max-width: 1300px;
  margin-block: 2rem;
  gap: 2rem;
}

img {
  max-width: 100%;
  display: block;
  object-fit: cover;
}

.card {
  display: flex;
  flex-direction: column;
  width: clamp(20rem, calc(20rem + 2vw), 22rem);
  overflow: hidden;
  box-shadow: 0 .1rem 1rem rgba(0, 0, 0, 0.1);
  border-radius: 1em;
  background: #ECE9E6;
background: linear-gradient(to right, #FFFFFF, #ECE9E6);

}
.card h4 {
  margin-block: 0.5rem;
  font-size: 1.5rem;
  font-weight: 700;
  color: #333;
  padding: 1rem 1rem 0 1rem;
}
.card p {
    margin-block: 0.5rem;
    font-size: 1rem;
    font-weight: 400;
    color: #333;
    padding: 0 1rem 1rem 1rem;
    }
.card__footer {
    padding: 1rem 1rem 0 1rem;
}
.card__footer h5 {
    padding-bottom:0;
    }
.tag {
    padding: 1rem;
    font-size: 0.75rem;
    font-weight: 700;
    color: #333;
    text-transform: uppercase;
    letter-spacing: 0.1rem;
    }
</style>
''', unsafe_allow_html=True)


st.markdown(f'''
<div class="containercard">
  <div class="card">
    <div class="card__header">
      <img src="https://source.unsplash.com/600x400/?computer" alt="card__image" class="card__image" width="600">
    </div>
    <div class="card__body">
      <span class="tag">Technology</span>
      <h4>What's new in 2022 Tech</h4>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sequi perferendis molestiae non nemo doloribus. Doloremque, nihil! At ea atque quidem!</p>
    </div>
    <div class="card__footer">
      <div class="user">
        <img src="https://i.pravatar.cc/40?img=1" alt="user__image" class="user__image">
        <div class="user__info">
          <h5>Jane Doe</h5>
          <small>2h ago</small>
        </div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card__header">
      <img src="https://source.unsplash.com/600x400/?food" alt="card__image" class="card__image" width="600">
    </div>
    <div class="card__body">
      <span class="tag">Food</span>
      <h4>Delicious Food</h4>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sequi perferendis molestiae non nemo doloribus. Doloremque, nihil! At ea atque quidem!</p>
    </div>
    <div class="card__footer">
      <div class="user">
        <img src="https://i.pravatar.cc/40?img=2" alt="user__image" class="user__image">
        <div class="user__info">
          <h5>Jony Doe</h5>
          <small>Yesterday</small>
        </div>
      </div>
    </div>
  </div>
  <div class="card">
    <div class="card__header">
      <img src="https://source.unsplash.com/600x400/?car,automobile" alt="card__image" class="card__image" width="600">
    </div>
    <div class="card__body">
      <span class="tag">Automobile</span>
      <h4>Race to your heart content</h4>
      <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Sequi perferendis molestiae non nemo doloribus. Doloremque, nihil! At ea atque quidem!</p>
    </div>
    <div class="card__footer">
      <div class="user">
        <img src="https://i.pravatar.cc/40?img=3" alt="user__image" class="user__image">
        <div class="user__info">
          <h5>John Doe</h5>
          <small>2d ago</small>
        </div>
      </div>
    </div>
  </div>
</div>
''', unsafe_allow_html=True)
