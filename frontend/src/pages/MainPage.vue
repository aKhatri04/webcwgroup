<template>
  <div class="h1">
    {{ title }}
  </div>
  <pre> {{  }}</pre>
      <!-- Edit ActorModal -->
    <!-- Edit actor modal, for all attributes under the actor model -->
    <div class="modal fade" id="editUserModal" tabindex="-1" aria-labelledby="editUserModalLabel" aria-hidden="true">
      <div class="modal-dialog">
          <div class="modal-content">
          <div class="modal-header">
              <h1 class="modal-title fs-5" id="exampleModalLabel">Edit Actor</h1>
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
                  <label for="date_of_birth" class="form-label"> Date of Birth </label>
                  <input v-model="changeUser.date_of_birth" type="date" class="form-control" id="date_of_birth">
              </div>
              <!--PLEASE CHECK IF THE OPTION TAG IS THE RIGHT ONE TO TAG TO REFER TO THE THROGUH MODEL IF WE CHANGE IT FROM THERE WITH MITHY -->
              <div class="mb-3">
                  <label for="hobby" class="form-label">Hobbies</label>
                  <select id="hobby" class="form-select" v-model="selectHobby">
                  <option v-for="hobby in changeUser.hobbies" key="hobby" :value="hobby">
                    {{ hobby.name }}
                  </option> 
                  </select>
              </div>
              <div class="mb-3">
                  <label for="newHobby" class="form-label">Add Hobby</label>
                  <input v-model="addHobby" type="text" class="form-control" id="newHobby" placeholder="Type a new hobby here" />
                  <button class="btn btn-primary mt-2" @click="addHobby">Add Hobby</button>
              </div>
              <div class="mb-3">
                  <label for="password" class="form-label">Password</label>
                  <input v-model="changeUser.password" type="password" class="form-control" id="password" placeholder="Leave blank to keep the same">
              </div>
          </div>
          <div class="modal-footer">
              <!-- Buttons implemented in the modal, a close and save button */ -->
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
              <button type="button" class="btn btn-primary" @click="editUser" data-bs-dismiss="modal">Save</button>
          </div>
          </div>
      </div>
      </div>

  
    <!-- UserModal -->
  <table class="table">
      <!-- Positioning of table for actors into columns -->
      <thead>
          <tr>
              <th scope="col">#</th>
              <th scope="col">Name</th>
              <th scope="col">Email</th>
              <th scope="col">Date of Birth</th>
              <th scope="col">Hobbies</th>
              <th scope="col">Password</th>
          </tr>
      </thead>
      <tbody>
          <!-- For all data in actor database, display with index id incrementing-->
          <tr v-for="(user, index) in users">
              <th scope="row">{{ index+1 }}</th>
              <td>
                  {{ user.name }}
              </td>
              <td>
                    {{ user.email }}
              </td>
              <td>
                    {{ user.date_of_birth }}
              </td>
              <td>
                <ul>
                  <!-- THIS NEED 100% CHEKC WITH MITHY!-->
                  <li v-for="hobby in user.hobbies" :key="hobby.id">
                      {{ hobby.name }}
                  </li>
                </ul>
              </td>
              <td>
                  <i>{{ user.password }}</i>
              </td>
              <td>
                  <!-- A button to edit actor under the content of the modal -->
                    
                  <button 
                      class="btn btn-sm btn-primary me-2"
                      data-bs-toggle="modal"
                      data-bs-target="#editUserModal"
                      @click="selectUser(user)"

                  >
                      Edit
                  </button>
              </td>
          </tr>
      </tbody>
  </table>

  <ActorTable
            :users = "users"
            @update="update"
        />
</template>

  
<script lang="ts">
    const baseUrl = 'http://localhost:8000'
    import { defineComponent } from "vue";

    interface User {
            id: string;
            name: string;
            email: string;
            date_of_birth: string;
            hobbies: Hobby[];
            password: string;
        }

    interface Hobby {
        id: number;
        name: string;
    }

    interface UserHobby {
        id: number;
        user_id: number;
        hobby_id: number;
    }

    export default defineComponent({
      emits: ['update'],
        props: {
            users: {
                type: Array as () => User[],
                required: true
            }
        },


        data() {
          
          // ASK MITHY AUTHENTICATION HE SAID PUT IN DATA 
          // computed: {
          //     csrfToken(): string {
          //       const cookies = document.cookie.split('; ');
          //       const csrfCookie = cookies.find((cookie) => cookie.startsWith('csrftoken='));
          //       return csrfCookie ? csrfCookie.split('=')[1] : '';
          //     },
          //   },

            return {
              // title: 'Actors',
              //   actors: [],
              //   newActor: {
              //       name:'',
              //       bio:'',
              //       acting:'',
              //       birth_date:'',
              //   }, NOT SURE WHETHER TO ADD - ASK MITHY
                title: "Welcome to your profile page, ${this.newUser.name}",
                // newUser: {
                //     name: "",
                //     email: "",
                //     date_of_birth: "",
                //     password: ""
                // },
                users: [] as User[],
                hobbies: [] as Hobby[],
                user_hobbies: [] as UserHobby[],
                changeUser: {
                    id: "",
                    name: "",
                    email: "",
                    date_of_birth: "",
                    hobbies: [] as Hobby[],
                    password: ""
                },
                addHobby:{
                    name: ""
                }
            }
        },

        //FETCHING SEEMS TO NOT WORK BUT THE LAYOUT IS ALL THERE, JUST PROB NEED SOME TWEAKS AND ASK MITHY
        async mounted() {
            const response = await fetch(`${baseUrl}/users`)

            const data = await response.json()
            this.users = data.users;
        },

        methods:{
            async editUser() {
                const response = await fetch(`${baseUrl}/users/${this.changeUser.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.changeUser)
                })
                //CHECK THE LINE BELOW TOO AND THE SAME WITH NEXT THREE FUNCTIONS BELOW
                // const user = await response.json()

                if (response.ok) {
                    this.$emit('update')
                    //I DONT KNOW IF NEED LINE BELOW ASK MITHY
                    //this.user.push(data);
                    alert('User updated successfully')
                }
            },

            async editHobby() {
                const response = await fetch(`${baseUrl}/user_hobbies/${this.changeUser.id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.changeUser)
                })
                // const user_hobbies = await response.json()

                if (response.ok) {
                    this.$emit('update')
                    //I DONT KNOW IF NEED LINE BELOW ASK MITHY
                    //this.hobbies.push(data);
                    alert('Hobby updated successfully')
                }
            },

            async addHobby() {
                const response = await fetch(`${baseUrl}/hobbies`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(this.addHobby)
                })
                // const hobbies = await response.json()

                if (response.ok) {
                    this.$emit('update')
                    //I DONT KNOW IF NEED LINE BELOW ASK MITHY
                    //this.hobbies.push(data);
                }
            },
            selectUser(user: User) {
                this.changeUser.id = user.id
                this.changeUser.name = user.name
                this.changeUser.email = user.email
                this.changeUser.date_of_birth = user.date_of_birth
                this.changeUser.hobbies = [...user.hobbies];
                this.changeUser.password = user.password
            },

            selectHobby(hobby: Hobby) {
                this.changeUser.hobbies.push(hobby);
            },

            async update() {
                const response = await fetch(`${baseUrl}/users/`)
                const data = await response.json()
                this.users = data.users;
                const response2 = await fetch (`${baseUrl}/hobbies`)
                const data2 = await response2.json()
                this.hobbies = data2.hobbies;
                const response3 = await fetch (`${baseUrl}/user_hobbies`)
                const data3 = await response3.json()
                this.user_hobbies = data3.user_hobbies;
            },
            }
        }
    )
</script>

<style scoped>
.add-actor-btn {
  background-color: #F4C2C2; 
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 4px;
  padding: 8px 16px;
  cursor: pointer;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.add-actor-btn:hover {
  background-color: #e8b1b1; 

}
</style>