const initialState = JSON.parse(localStorage.getItem("auth") || "{}")

export default function(state = initialState, action) {
  switch(action.type){
    case "AUTH_LOG_IN":
      return action.payload
    case "AUTH_LOG_OUT":
      return {}
    default:
      return state
  }
}
