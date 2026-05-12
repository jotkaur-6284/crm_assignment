import { createSlice } from '@reduxjs/toolkit'

const initialInteraction = {
  id: null,
  name: '',
  type: '',
  date: '',
  time: '',
  topic: '',
  material: '',
  sample: '',
  sentiment: '',
  outcomes: '',
}

const initialState = {
  currentInteraction: initialInteraction,
  messages: [],
  savedInteractions: [],
}

const interactionSlice = createSlice({
  name: 'interaction',
  initialState,
  reducers: {
    setInteraction(state, action) {
      state.currentInteraction = { ...initialInteraction, ...action.payload }
    },
    updateField(state, action) {
      const { field, value } = action.payload
      state.currentInteraction[field] = value
    },
    addMessage(state, action) {
      state.messages.push(action.payload)
    },
    setMessages(state, action) {
      state.messages = action.payload
    },
    setSavedInteractions(state, action) {
      state.savedInteractions = action.payload
    },
    resetInteraction(state) {
      state.currentInteraction = { ...initialInteraction }
    },
  },
})

export const {
  setInteraction,
  updateField,
  addMessage,
  setMessages,
  setSavedInteractions,
  resetInteraction,
} = interactionSlice.actions

export default interactionSlice.reducer
