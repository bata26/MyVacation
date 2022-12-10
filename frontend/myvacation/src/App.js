import React from "react";
import {
 BrowserRouter as Router,
 Routes,
 Route,
} from "react-router-dom";
import SignIn from "./pages/signIn";
import ResponsiveAppBar from "./components/navBar.js";
import {useEffect} from 'react';
import SignUp from "./pages/signUp";
import Profile from "./pages/profile";
import Home from "./pages/home/home"
import Checkout from "./pages/checkout/checkout"
import Search from "./pages/search"
import AdminPage from "./pages/adminPage/adminPage";
import Chart from "./pages/adminPage/chart";
import InsertAccomodation from "./pages/insertAccomodation";
import  Accomodation from "./pages/accomodation";
import  Activity from "./pages/activity";

function App() {
  useEffect(() => {
    document.body.style.margin = 0;

    return () => {  };
  }, []);

  return (
      <>
        <ResponsiveAppBar />
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/signin" element={<SignIn />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/profile/:profileID" element={<Profile />} />
            <Route path="/search" element={<Search />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/accomodation/:accomodationID" element={<Accomodation />} />
            <Route path="/edit/accomodation/:accomodationID" element={<InsertAccomodation />} />
            <Route path="/activity/:activityID" element={<Activity />} />
            {/*<Route element={<RequireAuth allowedRoles={"Admin"} />}>*/}
            <Route path="/admin" element={<AdminPage />} />
            <Route path="/reports" element={<Chart />} />
            {/*<Route path='/accomodationtobe/:id' element={<AccomodationToBe />}/>*/}
        </Routes>
      </>
  );
}

export default App;