import React, {Component} from 'react';
import styled from 'styled-components';
import styles from './App.css';
import { subscribeToTimer } from '../api';

// Our single Styled Component definition
const AppContainer = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  position: fixed;
  width: 100%;
  height: 100%;
  font-size: 40px;
  background: linear-gradient(20deg, rgb(219, 112, 147), #daa357);
`;

class App extends Component {
	constructor(props) {
		super(props);
		this.state = { timestamp: 'no timestamp yet' };
		subscribeToTimer((err, timestamp) => this.setState({ 
			timestamp 
		}));
	};

	render() {
		return (
			<AppContainer class="${styles.AppContainer}">
			    <div className="App">
					<p className="App-intro">
						This is the timer value: {this.state.timestamp}
					</p>
			    </div>
			</AppContainer>
		);
	}
} 

export default App;