<template>
    <!-- Edit Profile Modal -->
    <div class="modal fade" id="editProfileModal" tabindex="-1" aria-labelledby="editProfileModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5">Edit Profile</h1>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="mb-3">
              <label for="name" class="form-label">Name</label>
              <input v-model="changeUser.name" type="text" class="form-control" id="name">
            </div>
            <div class="mb-3">
              <label for="email" class="form-label">Email</label>
              <input v-model="changeUser.email" type="email" class="form-control" id="email">
            </div>
            <div class="mb-3">
              <label for="date_of_birth" class="form-label">Date of Birth</label>
              <input v-model="changeUser.date_of_birth" type="date" class="form-control" id="date_of_birth">
            </div>
            <div class="mb-3">
              <label for="password" class="form-label">Password (leave blank to keep current)</label>
              <input v-model="changeUser.password" type="password" class="form-control" id="password">
            </div>
            <div class="mb-3">
              <label for="hobbies" class="form-label">Hobbies</label>
              <ul>
                <li v-for="(hobby, index) in changeUser.hobbies" :key="hobby.id">
                  {{ hobby.name }}
                  <button @click="removeHobby(index)" class="btn btn-sm btn-danger ms-2">Remove</button>
                </li>
              </ul>
              <input v-model="newHobby" placeholder="Add new hobby" class="form-control mt-2" />
              <button @click="addHobby" class="btn btn-primary mt-2">Add Hobby</button>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-primary" @click="editProfile" data-bs-dismiss="modal">Save</button>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Profile Table -->
    <table class="table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Email</th>
          <th>Date of Birth</th>
          <th>Hobbies</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td>{{ user.name }}</td>
          <td>{{ user.email }}</td>
          <td>{{ user.date_of_birth }}</td>
          <td>
            <span v-for="hobby in user.hobbies" :key="hobby.id" class="badge bg-secondary me-1">{{ hobby.name }}</span>
          </td>
          <td>
            <button class="btn btn-sm btn-primary" data-bs-toggle="modal" data-bs-target="#editProfileModal">
              Edit
            </button>
          </td>
        </tr>
      </tbody>
    </table>
  </template>
  
  <script>
  const baseUrl = 'http://localhost:8000';
  
  export default {
    props: {
      user: Object,
    },
    data() {
      return {
        changeUser: { ...this.user, password: '', hobbies: [...this.user.hobbies] },
        newHobby: '',
      };
    },
    methods: {
      async editProfile() {
        const response = await fetch(`${baseUrl}/api/user/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.changeUser),
        });
        if (response.ok) {
          this.$emit('update');
        }
      },
      addHobby() {
        if (this.newHobby.trim()) {
          this.changeUser.hobbies.push({ name: this.newHobby });
          this.newHobby = '';
        }
      },
      removeHobby(index) {
        this.changeUser.hobbies.splice(index, 1);
      },
    },
  };
  </script>
  
  <style scoped>
  td, th {
    vertical-align: middle;
  }
  </style>
  