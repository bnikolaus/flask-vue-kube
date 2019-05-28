<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>Tasks</h1>
        <hr><br><br>
        <alert :message=message v-if="showMessage"></alert>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.task-modal>Add Task</button>
        <br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Description</th>
              <th scope="col">Team</th>
              <th scope="col">Planned</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(task, index) in tasks" :key="index">
              <td>{{ task.description }}</td>
              <td>{{ task.team }}</td>
              <td>
                <span v-if="task.planned">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <button
                        type="button"
                        class="btn btn-warning btn-sm"
                        v-b-modal.task-update-modal
                        @click="editTask(task)">
                    Update
                </button>
                <button
                        type="button"
                        class="btn btn-danger btn-sm"
                        @click="onDeleteTask(task)">
                    Delete
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <b-modal ref="addTaskModal"
             id="task-modal"
             description="Add a new task"
             hide-footer>
      <b-form @submit="onSubmit" @reset="onReset" class="w-100">
      <b-form-group id="form-description-group"
                    label="Description:"
                    label-for="form-description-input">
          <b-form-input id="form-description-input"
                        type="text"
                        v-model="addTaskForm.description"
                        required
                        placeholder="Enter description">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-team-group"
                      label="Team:"
                      label-for="form-team-input">
            <b-form-input id="form-team-input"
                          type="text"
                          v-model="addTaskForm.team"
                          required
                          placeholder="Enter team">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-planned-group">
          <b-form-checkbox-group v-model="addTaskForm.planned" id="form-checks">
            <b-form-checkbox value="true">Planned</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Submit</b-button>
        <b-button type="reset" variant="danger">Reset</b-button>
      </b-form>
    </b-modal>
    <b-modal ref="editTaskModal"
             id="task-update-modal"
             description="Update"
             hide-footer>
      <b-form @submit="onSubmitUpdate" @reset="onResetUpdate" class="w-100">
      <b-form-group id="form-description-edit-group"
                    label="Description:"
                    label-for="form-description-edit-input">
          <b-form-input id="form-description-edit-input"
                        type="text"
                        v-model="editForm.description"
                        required
                        placeholder="Enter description">
          </b-form-input>
        </b-form-group>
        <b-form-group id="form-team-edit-group"
                      label="Author:"
                      label-for="form-team-edit-input">
            <b-form-input id="form-team-edit-input"
                          type="text"
                          v-model="editForm.team"
                          required
                          placeholder="Enter team">
            </b-form-input>
          </b-form-group>
        <b-form-group id="form-planned-edit-group">
          <b-form-checkbox-group v-model="editForm.planned" id="form-checks">
            <b-form-checkbox value="true">Read?</b-form-checkbox>
          </b-form-checkbox-group>
        </b-form-group>
        <b-button type="submit" variant="primary">Update</b-button>
        <b-button type="reset" variant="danger">Cancel</b-button>
      </b-form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios';
import Alert from './Alert';

export default {
  data() {
    return {
      tasks: [],
      addTaskForm: {
        description: '',
        team: '',
        planned: [],
      },
      editForm: {
        id: '',
        description: '',
        team: '',
        planned: [],
      },
      message: '',
      showMessage: false,
      ROOT_API: process.env.ROOT_API,
    };
  },
  components: {
    alert: Alert,
  },
  methods: {
    getTasks() {
      const path = `${this.ROOT_API}/tasks`;
      axios.get(path)
        .then((res) => {
          this.tasks = res.data.tasks;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    addTask(payload) {
      const path = `${this.ROOT_API}/tasks`;
      axios.post(path, payload)
        .then(() => {
          this.getTasks();
          this.message = 'Task added!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getTasks();
        });
    },
    updateTask(payload, taskID) {
      const path = `${this.ROOT_API}/tasks/${taskID}`;
      axios.put(path, payload)
        .then(() => {
          this.getTasks();
          this.message = 'Task updated!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getTasks();
        });
    },
    removeTask(taskID) {
      const path = `${this.ROOT_API}/tasks/${taskID}`;
      axios.delete(path)
        .then(() => {
          this.getTasks();
          this.message = 'Task removed!';
          this.showMessage = true;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getTasks();
        });
    },
    initForm() {
      this.addTaskForm.description = '';
      this.addTaskForm.team = '';
      this.addTaskForm.planned = [];
      this.editForm.id = '';
      this.editForm.description = '';
      this.editForm.team = '';
      this.editForm.planned = [];
    },
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.addTaskModal.hide();
      let planned = false;
      if (this.addTaskForm.planned[0]) planned = true;
      const payload = {
        description: this.addTaskForm.description,
        team: this.addTaskForm.team,
        planned, // property shorthand
      };
      this.addTask(payload);
      this.initForm();
    },
    onSubmitUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTaskModal.hide();
      let planned = false;
      if (this.editForm.planned[0]) planned = true;
      const payload = {
        description: this.editForm.description,
        team: this.editForm.team,
        planned,
      };
      this.updateTask(payload, this.editForm.id);
    },
    onReset(evt) {
      evt.preventDefault();
      this.$refs.addTaskModal.hide();
      this.initForm();
    },
    onResetUpdate(evt) {
      evt.preventDefault();
      this.$refs.editTaskModal.hide();
      this.initForm();
      this.getTasks(); // why?
    },
    onDeleteTask(task) {
      this.removeTask(task.id);
    },
    editTask(task) {
      his.editForm = task;
    },
  },
  created() {
    this.getTasks();
  },
};
</script>
