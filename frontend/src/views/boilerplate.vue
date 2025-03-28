<template>
    <div class="container">
    <div class="admin-dashboard">
              <RouterLink to="/admindash" class="disabled">
                <i class="fas fa-home"> Home</i>
              </RouterLink>
              <RouterLink to="/admindash/subjects" class="icon">
                <i class="fas fa-book circular-icon">  Subjects</i>
              </RouterLink>
              <RouterLink to="/admindash/user" class="icon">
                <i class="fas fa-user circular-icon">  Users</i>
                </RouterLink>
              <RouterLink to="/admindash/stats" class="icon">
                <i class="fas fa-chart-bar">  Stats</i>
              </RouterLink>
              <a href="#" @click.prevent="logout" class="icon">
                <i class="fas fa-sign-out-alt">  Log Out</i>
              </a>
    </div>
  </div>
</template>



<style>
html, body, #app {
  margin: 0;
  width: 100%;
}

.container {
    font-family: 'Times New Roman', Times, serif;
  display: flex;
  background-color: rgb(213, 213, 213);
  width: 100%;
}

.admin-dashboard {
  display: flex;
  background-color: rgb(56, 56, 56);
  flex-direction: column;
  justify-content: center;
  padding: 10px;
  align-items: flex-start;
  width: 250px;
}
.icon {
    display: flexbox;
    justify-content: center;
    align-items: flex-start;
    padding: 10px;
    border-radius: 250px;
    margin:10px;
    color: rgb(255, 255, 255);
    width: 80%;
    font-family: 'Times New Roman', Times, serif;
}
.icon:hover {
  background-color: #000000;
  transform: scale(1.1);
}
.disabled{
    background-color: rgb(117, 116, 116);
    padding: 10px;
    border-radius: 250px;
    margin:10px;
    width: 80%;
    color:aliceblue;
}

</style>