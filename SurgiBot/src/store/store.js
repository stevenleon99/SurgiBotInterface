import Vuex from 'vuex'

export default new Vuex.Store({
    state: {
      count: 6,
      joint: [0,0,0,0,0,0],
      joint_real: [0,0,0,0,0,0],
    },
    mutations: {
      increment (state) {
        state.count++;
      },
      updatejoint(state, newjoint) {
        state.joint = newjoint.joints;
      },
      updatejoint_real(state, newjoint) {
        state.joint_real = newjoint.joints;
      },
    }
});
