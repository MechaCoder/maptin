import React, { Component } from "react";
import ReactDOM from "react-dom";

import Draggable from 'react-draggable';
import { io } from "socket.io-client";

export default class Vtoken extends Component {
    constructor() {
        super();
        this.state = {
            'opacity': '100%',
            'connection': false,
            'x': 0,
            'y': 100
        }
        this.updateLocation = this.updateLocation.bind(this);
    }

    componentDidMount(){
        this.socket = io();

        this.socket.on('connect', ()=>{
            // this.socket.join(this.props.hex)

            this.setState({
                'opacity': '100%',
                'connection': true
            })
        })

        this.socket.on('message', (_data)=>{
            // console.log(this.props.hex != _data.hex)1
            var json = JSON.parse(_data);
            console.log(json)

            if(this.props.hex != json.hex){
                console.log('not this one')
                return;
            }
            // return;
            this.setState({
                x: json.x,
                y: json.y
            })
        })

        this.socket.on('disconnect', ()=>{
            this.setState({
                'opacity': '50%',
                'connection': false
            })
        })

        this.setState({
            'x':this.props.x,
            'y':this.props.y
        })
        
    }

    updateLocation(e, _data){
        this.socket.emit('message', JSON.stringify({
            hex: this.props.hex,
            x: _data.x,
            y: _data.y
        }));

        this.setState({
            x: _data.x,
            y: _data.y
        })
    }

    render() {
        return (
            <Draggable 
                defaultPosition={{x: this.state.x, y: this.state.y}}
                position={{x: this.state.x, y: this.state.y}} 
                onStop={this.updateLocation} 
                disabled={!this.state.connection} 
            >
                <div className='daggabletoken' style={{opacity: this.state.opacity}}>
                    <img src={this.props.pic} width='15px' />
                </div>
            </Draggable>
        )
    }
}