import React, { Component } from 'react';
import ReactDropzone from 'react-dropzone';
import { IoMdCloudUpload } from 'react-icons/io';
import { IconContext } from 'react-icons';
import { Line } from 'rc-progress';
import io from 'socket.io-client'
import axios from 'axios';
import './App.css';

const serverUrl = 'http://127.0.0.1:7072/';

class App extends Component {

  constructor() {
    super();
    this.state = {
      progress: 0,
      showDropzone: true,
      fileName: 'Drop or Select a file',
    }
  }

  onDrop = (files) => {
    console.log(files);
    var fileMd5 = '';

    var socket = io(serverUrl, { transports: ['websocket'] });
    socket.on('error', function(res){
      console.log(res)
    })
    socket.on('status_update', function(res) {
      console.log("Current Status: " + res.status);
      switch(res.status) {
        case "1":
          this.setState({
            progress: '25'
          })
          break;
        case "2":
          this.setState({
            progress: '50'
          })
          break;
        case "3":
          this.setState({
            progress: '75'
          })
          break;
        case "4":
          this.setState({
            progress: '100'
          })
          break;
        default:
          this.setState({
            progress: '0'
          })
          break;
      }
    })

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
          showDropzone: false,
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
          (error) => console.log(error)
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
        { this.state.showDropzone ? 
          <ReactDropzone 
            accept="application/x-gzip"
            onDrop={this.onDrop} 
            className="dropzone"
          >
            <IconContext.Provider value={{ size: "5em" }}>
              <IoMdCloudUpload/>
            </IconContext.Provider>
          <h1>{this.state.fileName}</h1>
        </ReactDropzone>
        :
        <div className="convertzone"> 
          Converting { this.state.fileName } 
          <Line percent={ this.state.progress } strokeWidth="2" strokeColor="#2dc663"/>
          Progress: { this.state.progress }%
        </div>
      }  
      </div>
    );
  }
}

export default App;