import React from "react";
import Landing from './Landing.js';
import Idea from './Idea.js';
import About from './About.js';
import Current_Work from "./Current_Work.js";
import Navbar from '../components/Navbar';
import Login from './Login.js';

function Main() {
	return (
		<div>
			<Navbar />
			<Landing/>
			<Idea/>
			<Current_Work/>
			<Login/>
			// <About/>
		</div>
	)
}

export default Main
