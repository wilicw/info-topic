import Vue from 'vue';
import Vuex from 'vuex';

Vue.use(Vuex);

const store = new Vuex.Store({
    state: {
        is_login: false,
        popup: {
            state: "none",
            msg: ""
        },
    },
    mutations: {
        login(state) {
            state.is_login = true
        },
        logout(state) {
            state.is_login = false
        },
        show_popup(state, { s, msg }) {
            state.popup.state = s
            state.popup.msg = msg
        }
    }
})
export default store;