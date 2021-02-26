import React, { Component } from "react";
import ReactDOM from "react-dom";

import Draggable from 'react-draggable';
import {io} from 'socket.io-client';

export default class Vtoken extends Component {
    
    constructor() {
        super();
        this.state = {
            'opacity': '100%',
            'connection': false,
            'x': 0,
            'y': 100,
            'hide': false
        }
        this.updateLocation = this.updateLocation.bind(this);
        this.deleteMe = this.deleteMe.bind(this)
    }

    componentDidMount(){
        this.socket = io();

        this.socket.on('connect', ()=>{

            this.setState({
                'opacity': '100%',
                'connection': true
            })
        })

        this.socket.on('message', (_data)=>{
            var json = JSON.parse(_data);

            if(this.props.hex != json.hex){
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
        this.socket.on('vtoken:remove', (_data) => {
            if(this.props.hex == _data.hex){
                this.setState({'hide': true})
            }

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

    deleteMe(e){    

        var obj = confirm('are you sure you what to delete?')
        if(!obj){
            return;
        }

        fetch('/ajax/token', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'hex': this.props.hex
            }
        })
        .then(data => data.json())
        .then((json)=>{
            if(json.succ){
                this.setState({
                    'connection': false,
                    'hide': true
                })
            }
        })

    }

    render() {
        var parent_css = {opacity: this.state.opacity}
        if(this.state.hide){
            parent_css.display = 'none'
        }

        return (
            <Draggable 
                defaultPosition={{x: this.state.x, y: this.state.y}}
                position={{x: this.state.x, y: this.state.y}} 
                onStop={this.updateLocation} 
                disabled={!this.state.connection} 
            >
                <div className='daggabletoken' style={parent_css}>
                    <img src={this.props.pic} width='15px' />
                    <div className="tools">
                        <a href='/' onClick={(e)=>{e.preventDefault(); this.deleteMe(e)}}>x</a>  
                    </div>
                </div>
            </Draggable>
        )
    }
}