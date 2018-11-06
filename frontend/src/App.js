import React, { Component } from 'react';
import ReactDropzone from 'react-dropzone';
import { IoMdCloudUpload } from 'react-icons/io';
import { IconContext } from 'react-icons';
import { Line } from 'rc-progress';
import SparkMD5 from 'spark-md5'
import openSocket from 'socket.io-client';
import axios from 'axios';
import './App.css';

const serverUrl = 'http://127.0.0.1:7075/';

class App extends Component {

  constructor() {
    super();
    
    this.state = {
      action: 'Received',
      progress: 0,
      showDropzone: true,
      fileName: 'Drop or Select a file',
    }
  }

  componentDidMount() {
    // Initialize the socket and listen to correct events
    const socket = openSocket(serverUrl)

    socket.on('status_update', (res) => {
      console.log("Current Status: " + res);
      switch(res) {
        case "1":
          this.setState({
            action: 'Uploading',
            progress: '25'
          })
          break;
        case "2":
          this.setState({
            action: 'Extracting',
            progress: '50'
          })
          break;
        case "3":
          this.setState({
            action: 'Converting',
            progress: '75'
          })
          break;
        case "4":
          this.setState({
            action: 'Packing',
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
  }

  onDrop = (files) => {
    var fileMd5 = '';

    files.forEach(file => {
      this.setState({
        showDropzone: false,
        fileName: file.name,
      })
      console.log(file)
      const reader = new FileReader();

      reader.onabort = () => console.log('file reading was aborted');
      reader.onerror = () => console.log('file reading has failed');
      reader.onload = () => {
        var spark = new SparkMD5();

        const fileAsBinaryString = reader.result;

        spark.appendBinary(fileAsBinaryString);
        fileMd5 = spark.end();

        var bucketName = file.name.split(".")[0];

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
          (res) => {
            console.log(res) 
          }
        ).catch(
          (error) => {
            this.setState({
              showDropzone: true,
              fileName: error.response.data.message,
            })
            console.log(error.response)
          }
        )
      }

      try {
        reader.readAsBinaryString(file);
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
          {this.state.action} { this.state.fileName } 
          <Line percent={ this.state.progress } strokeWidth="2" strokeColor="#2dc663"/>
          Progress: { this.state.progress }%
        </div>
      }  
      </div>
    );
  }
}

export default App;