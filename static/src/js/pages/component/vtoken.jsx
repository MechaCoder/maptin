import React, { Component } from "react";
import ReactDOM from "react-dom";

import {getUserId, userIdExists, getMapHexFromURL} from './commons.jsx';
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
            'hide': false,
            'conseal': false,
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

        this.socket.on('vtoken:conseal', (_data) => {
            // return;

            if(_data.uhex == this.props.hex){
                this.setState({
                    'conseal': _data['conseal']
                })
                console.log('three')
            }

        })

        this.setState({
            'x':this.props.x,
            'y':this.props.y,
            'conseal': this.props.conseal
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
            } else {
                alert(json.err)
            }
        })

    }

    updateConseal(e){
        e.preventDefault()

        console.log('1')

        this.socket.emit('vtoken:conseal', {
            'uhex': this.props.hex,
            'conseal': this.state.conseal,
        });
    }

    render() {
        var parent_css = {opacity: this.state.opacity}

        if(this.state.hide){
            parent_css.display = 'none'
        }

        if(this.state.conseal){
            parent_css.opacity = '20%'

            if(userIdExists()===false){
                parent_css.display = 'none'
            }
        }

        var dmTools = []

        if(userIdExists()){
            var buttonText = ()=>{ if(this.state.conseal){return 'show'} return 'hide';}

            dmTools.push(
                <button onClick={(e) => { e.preventDefault(); this.updateConseal(e)}}>
                    {buttonText()}
                </button>
            )
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
                        <button onClick={(e)=>{e.preventDefault(); this.deleteMe(e)}}>Delete</button>
                        {dmTools}
                    </div>
                </div>
            </Draggable>
        )
    }
}