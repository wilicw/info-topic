import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        is_login: false,
    },
    mutations: {
        login(state) {
            state.is_login = true
        }, logout(state) {
            state.is_login = false
        }
    }
})
export default store;