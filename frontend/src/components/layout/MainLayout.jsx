import React from 'react'
import { Outlet } from 'react-router-dom'

import NavBar from '../common/Navbar'
import Footer from '../common/Footer'

const MainLayout = () => {
  return (
    <>
      <NavBar />
      <main>
        <Outlet />
      </main>
      <Footer />
    </>
  )
}

export default MainLayout