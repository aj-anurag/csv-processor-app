<template>
    <div class="section">
      <div class="container">

        <simple-upload />

      </div>
    </div>
   </template>

    <script>
      import SimpleUpload from './SimpleUpload.vue';

  export default {
    name:"app",
    components: {SimpleUpload}
  };
    </script>
    <!-- <form action="http://127.0.0.1:8000/upload" method="post" enctype="multipart/form-data">
      <input type="file" id="myFile" name="filename">
      <input type="submit">
    </form> -->
