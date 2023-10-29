import React from "react";
import Landing from './Landing.js';
import Idea from './Idea.js';
import About from './About.js';
import Navbar from '../components/Navbar';

function Main() {
	return (
		<div>
			<Navbar />
			<Landing/>
			<Idea/>
			<About/>
		</div>
	)
}

export default Main
