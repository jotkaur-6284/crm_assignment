
import { useSelector } from 'react-redux'
import InteractionForm from './components/InteractionForm'
import ChatAssistant from './components/ChatAssistant'

export default function App() {
  const data = useSelector((state) => state.interaction.currentInteraction)

  return (
    <div className="container">
      <div className="left-panel">
        <InteractionForm data={data} />
      </div>

      <div className="right-panel">
        <ChatAssistant />
      </div>
    </div>
  )
}
