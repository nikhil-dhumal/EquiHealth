import { useState } from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

import routes from './routes/Routes.jsx'

const App = () => {
  const [count, setCount] = useState(0)

  return (
    <Router>
      <Routes>
        {
          routes.map(({ path, element }, index) => {
            <Route key={index} path={path} element={element} />
          })  
        }
      </Routes>
    </Router>
  )
}

export default App
