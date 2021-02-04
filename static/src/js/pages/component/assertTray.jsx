import React, { Component } from "react";
import ReactDOM from "react-dom";

function imgEl(src){
    return(<span className='asset' style={{backgroundImage: 'url(' + src + ')'}} ></span>)
}   

export default class AssertToken extends Component {
    constructor() {
        super();
        this.state = { 
            'tokens': []
        }
    }

    componentDidMount(){
        fetch(
            '/ajax/assets/' + this.props.subpath, 
            {headers: {'Content-Type': 'application/json'}
        })
        .then(data => data.json())
        .then((json) => {
            console.log(json)
            if(json.succs){
                // console.log(json.data)
                this.setState({'tokens': json.data})
            }
        })
    }

    render() {
        
        var els = []
        for(var i = 0; i<this.state.tokens.length; i++){
            // console.log(this.state.tokens[i])
            els.push( imgEl(this.state.tokens[i]) )      
        }

        var tray_width = (this.state.tokens.length * 100)

        return (
            <div className='AssertToken'>
                <div className='title'> AssertToken </div>
                <div className='tray' style={{'width': tray_width}}>{els}</div>
            </div>
        )
    }
}