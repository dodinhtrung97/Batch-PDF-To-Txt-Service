import React, { Component } from 'react';
import ReactDropzone from 'react-dropzone';
import { IoMdCloudUpload } from 'react-icons/io';
import { IconContext } from 'react-icons';
import './App.css';

class App extends Component {
  constructor() {
    super();
    this.state = {
      fileName: 'Drop or Select a file',
      fileMd5: '',
      fileSize: '',
    }
  }

  onDrop = (files) => {
    var fileMd5 = '';

    files.forEach(file => {
      const reader = new FileReader();
      reader.onload = () => {
        var md5 = require('md5');
        const fileAsBinaryString = reader.result;
        fileMd5 = md5(fileAsBinaryString);

        this.setState({
          fileName: file.name,
          fileMd5: fileMd5,
          fileSize: file.size
        })
      }
      reader.onabort = () => console.log('file reading was aborted');
      reader.onerror = () => console.log('file reading has failed');

      try {
        reader.readAsDataURL(file);
      } catch(err) {
        console.log(err);
      }
    });
  }

  render() {
    return (
      <div className="app">
        <ReactDropzone onDrop={e => this.onDrop(e)} className="dropzone">
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