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
import Home from "./pages/home";
import Checkout from "./pages/checkout";
import Search from "./pages/search";
import EditAccomodation from "./pages/editAccomodation";
import EditActivity from "./pages/editActivity";
import AdminPage from "./pages/adminPage/adminPage";
import InsertAccomodation from "./pages/insertAccomodation";
import  Accomodation from "./pages/accomodation";
import  Activity from "./pages/activity";
import InsertActivity from "./pages/insertActivity";
import MyAdv from "./pages/myAdv";
import ToApprove from "./pages/toApprove";
import Unauthorized from "./pages/unauthorized";

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
            <Route path="/signin" element={localStorage.getItem("userID") == null ? <SignIn /> : <Profile/>} />
            <Route path="/signup" element={localStorage.getItem("userID") == null ? <SignUp /> : <Profile/>} />
            <Route path="/profile/:profileID" element={localStorage.getItem("userID") != null ? <Profile /> : <Unauthorized/>} />
            <Route path="/myadv" element={localStorage.getItem("userID") != null ? <MyAdv /> : <Unauthorized/>} />
            <Route path="/search" element={<Search />} />
            <Route path="/checkout" element={<Checkout />} />
            <Route path="/accomodation/:accomodationID" element={<Accomodation />} />
            <Route path="/toApprove/:advertisementID" element={localStorage.getItem("role") === "admin" ? <ToApprove />: <Unauthorized/>} />
            <Route path="/insert/accomodation" element={localStorage.getItem("userID") != null ? <InsertAccomodation /> : <Unauthorized/>} />
            <Route path="/insert/activity" element={localStorage.getItem("userID") != null ? <InsertActivity /> : <Unauthorized/>} />
            <Route path="/edit/accomodation/:accomodationID" element={localStorage.getItem("userID") != null || localStorage.getItem("role") !== "admin" ? <EditAccomodation />: <Unauthorized/>} />
            <Route path="/edit/activity/:activityID" element={localStorage.getItem("userID") != null || localStorage.getItem("role") !== "admin" ? <EditActivity /> : <Unauthorized/>} />
            <Route path="/activity/:activityID" element={<Activity />} />
            <Route path="/admin" element={localStorage.getItem("role") === "admin" ? <AdminPage /> : <Unauthorized/>} />
        </Routes>
      </>
  );
}

export default App;