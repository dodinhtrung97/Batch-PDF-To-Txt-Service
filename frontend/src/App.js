import React, { Component } from 'react';
import ReactDropzone from 'react-dropzone';
import FileReader from 'filereader'
import { IoMdCloudUpload } from 'react-icons/io';
import { IconContext } from 'react-icons';
import './App.css';

class App extends Component {
  constructor() {
    super();
    this.state = {
      fileName: 'Drop or Select a file'
    }
  }

  onDrop = (files) => {
    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = () => {
        const fileAsBinaryString = reader.result
        console.log(fileAsBinaryString);
      }
      reader.onabort = () => console.log('file reading was aborted');
      reader.onerror = () => console.log('file reading has failed');

      reader.readAsDataURL(new File('./index.js'));

      this.setState({
        fileName: file.name
      })
    });
  }

  render() {
    return (
      <div className="app">
        <ReactDropzone onDrop={this.onDrop} className="dropzone">
          <IconContext.Provider value={{ size: "5em" }}>
            <IoMdCloudUpload/>
          </IconContext.Provider>
          <h1>{this.state.fileName}</h1>
        </ReactDropzone>
      </div>
    );
  }
}

export default App;
