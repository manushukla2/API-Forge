import { useState } from 'react'
import Sidebar from './components/Sidebar'
import HomeScreen from './screens/HomeScreen'
import QADashboard from './screens/QADashboard'
import ImportAPI from './screens/ImportAPI'
import TestRunner from './screens/TestRunner'
import Evidence from './screens/Evidence'
import Reports from './screens/Reports'
import DevDashboard from './screens/DevDashboard'
import Requirements from './screens/Requirements'
import StackAdvisor from './screens/StackAdvisor'
import Architecture from './screens/Architecture'
import ExportScreen from './screens/ExportScreen'

export default function App() {
  const [active, setActive] = useState('home')

  const screens = {
    home:         <HomeScreen navigate={setActive} />,
    qa_home:      <QADashboard navigate={setActive} />,
    doc_input:    <ImportAPI navigate={setActive} />,
    test_runner:  <TestRunner navigate={setActive} />,
    evidence:     <Evidence navigate={setActive} />,
    reports:      <Reports navigate={setActive} />,
    dev_home:     <DevDashboard navigate={setActive} />,
    requirements: <Requirements navigate={setActive} />,
    stack:        <StackAdvisor navigate={setActive} />,
    architecture: <Architecture navigate={setActive} />,
    export:       <ExportScreen navigate={setActive} />,
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: 'var(--background)', color: 'var(--foreground)' }}>
      <Sidebar active={active} navigate={setActive} />
      <main style={{ flex: 1, overflow: 'auto', minWidth: 0 }}>
        {screens[active] || screens['home']}
      </main>
    </div>
  )
}