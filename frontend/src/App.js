import React, { Component } from 'react';
import ReactDropzone from 'react-dropzone';
import { IoMdCloudUpload } from 'react-icons/io';
import { IconContext } from 'react-icons';
import axios from 'axios';
import './App.css';

const serverUrl = 'http://127.0.0.1:7072/';

class App extends Component {
  constructor() {
    super();
    this.state = {
      bucketName: '',
      fileName: 'Drop or Select a file',
      fileMd5: '',
      fileSize: '',
    }
  }

  onDrop = (files) => {
    console.log(files);
    var fileMd5 = '';

    files.forEach(file => {
      const reader = new FileReader();

      reader.onabort = () => console.log('file reading was aborted');
      reader.onerror = () => console.log('file reading has failed');
      reader.onload = () => {
        var md5 = require('md5');
        const fileAsBinaryString = reader.result;
        fileMd5 = md5(fileAsBinaryString);

        var bucketName = file.name.split(".")[0];
        this.setState({
          fileName: file.name,
        })

        // Upload request to bucket
        // Create bucket with name = fileName
        axios({
          method: 'post',
          url: serverUrl + bucketName + "/" + file.name,
          data: {
            fileMd5: fileMd5,
            fileSize: file.size,
            data: fileAsBinaryString
          }
        }).then( 
          (res) => console.log(res) 
        ).catch(
          console.log("Upload Failed")
        )
      }

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